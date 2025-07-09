import streamlit as st
import openai
import json
import logging
from datetime import datetime
import os
import io
from typing import List, Dict, Any
import tiktoken

from artefato_splitter_spring_boot import ArtefatoSplitterSpringBoot


# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chat_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ChatAssistant:
    def __init__(self):
        self.models = {
            "GPT-4o": "gpt-4o",
            "GPT-4.1": "gpt-4-turbo"
        }
        self.total_tokens = 0
        self.session_tokens = 0
        
    def count_tokens(self, text: str, model: str) -> int:
        """Conta tokens usando tiktoken"""
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception as e:
            logger.error(f"Erro ao contar tokens: {e}")
            return len(text.split()) * 1.3  # Estimativa aproximada
    
    def log_interaction(self, prompt: str, response: str, model: str, tokens_used: int, file_info: str = None):
        """Log das interações com o LLM"""
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "prompt": prompt,
            "response": response,
            "tokens_used": tokens_used,
            "file_info": file_info
        }
        logger.info(f"Interação registrada: {json.dumps(log_data, ensure_ascii=False)}")
    
    def process_file(self, uploaded_file) -> str:
        """Processa arquivo enviado"""
        try:
            if uploaded_file.type == "text/plain":
                content = str(uploaded_file.read(), "utf-8")
            elif uploaded_file.type == "application/pdf":
                st.warning("Para PDFs, você precisará instalar PyPDF2 ou similar")
                content = "Arquivo PDF carregado (processamento básico não implementado)"
            else:
                content = str(uploaded_file.read(), "utf-8")
            
            return content
        except Exception as e:
            logger.error(f"Erro ao processar arquivo: {e}")
            return f"Erro ao processar arquivo: {str(e)}"
    
    def send_message(self, messages: List[Dict], model: str, file_content: str = None, temperature: float = 0.7) -> Dict[str, Any]:
        """Envia mensagem para OpenAI"""
        try:
            # Adiciona conteúdo do arquivo se disponível
            if file_content:
                messages.append({
                    "role": "system",
                    "content": f"Arquivo enviado pelo usuário:\n\n{file_content}"
                })
            
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature  # Use a temperatura definida pelo usuário
                # max_tokens=1000
            )
            
            # Log da resposta convertendo para string
            logger.info("### Resposta do LLM ###\n" + str(response))
            
            # Contabiliza tokens
            prompt_tokens = response.usage.prompt_tokens
            completion_tokens = response.usage.completion_tokens
            total_tokens = response.usage.total_tokens
            
            self.total_tokens += total_tokens
            self.session_tokens += total_tokens
            
            # Salvando resulto em arquivos
            splitter = ArtefatoSplitterSpringBoot()
            splitter.split(response.choices[0].message.content,)
            
            return {
                "content": response.choices[0].message.content,
                "tokens": {
                    "prompt": prompt_tokens,
                    "completion": completion_tokens,
                    "total": total_tokens
                }
            }
        except Exception as e:
            logger.error(f"Erro na API OpenAI: {e}")
            return {"error": str(e)}
    
    def manage_context_window(self, messages: List[Dict], max_messages: int = 10) -> List[Dict]:
        """Gerencia janela de contexto mantendo mensagens mais recentes"""
        if len(messages) <= max_messages:
            return messages
        
        # Mantém a primeira mensagem do sistema (se existir) e as últimas mensagens
        system_messages = [msg for msg in messages if msg["role"] == "system"]
        user_assistant_messages = [msg for msg in messages if msg["role"] in ["user", "assistant"]]
        
        # Pega as últimas mensagens
        recent_messages = user_assistant_messages[-(max_messages-len(system_messages)):]
        
        return system_messages + recent_messages
    
    def clear_logs(self):
        """Limpa o arquivo de logs"""
        try:
            open('chat_logs.log', 'w').close()
            logger.info("Logs limpos na inicialização da aplicação")
        except Exception as e:
            logger.error(f"Erro ao limpar logs: {e}")

def main():
    st.set_page_config(
        page_title="Assistente de Chat OpenAI",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Assistente de Chat OpenAI")
    
    # Inicializar o assistente
    if 'assistant' not in st.session_state:
        st.session_state.assistant = ChatAssistant()
        st.session_state.assistant.clear_logs()  # Limpa logs na inicialização
    
    # Inicializar mensagens
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # API Key
        api_key = st.text_input("API Key OpenAI", type="password", 
                               help="Digite sua chave da API OpenAI")
        
        if api_key:
            openai.api_key = api_key
        
        # Seleção do modelo
        selected_model = st.selectbox(
            "Modelo GPT",
            options=list(st.session_state.assistant.models.keys()),
            index=0
        )
        
        # Upload de arquivo
        st.subheader("📁 Upload de Arquivo")
        uploaded_file = st.file_uploader(
            "Escolha um arquivo",
            type=['txt', 'pdf', 'docx', 'csv', 'json', 'md'],
            help="Faça upload de um arquivo para análise"
        )
        
        # Configurações do contexto
        st.subheader("🔧 Contexto")
        max_context_messages = st.slider(
            "Máximo de mensagens no contexto",
            min_value=5,
            max_value=20,
            value=10,
            help="Controla quantas mensagens mantém no contexto"
        )
        
        # Configurações de temperatura
        st.subheader("🌡️ Temperatura")
        temperature = st.slider(
            "Temperatura do modelo",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1,
            help="Controla a criatividade das respostas (0 = mais focado, 2 = mais criativo)"
        )
        
        # Botão para limpar contexto
        if st.button("🗑️ Limpar Contexto"):
            st.session_state.messages = []
            st.rerun()
        
        # Estatísticas de tokens
        st.subheader("📊 Consumo de Tokens")
        st.metric("Tokens da Sessão", st.session_state.assistant.session_tokens)
        st.metric("Total de Tokens", st.session_state.assistant.total_tokens)
        
        # Botão para reset de contadores
        if st.button("🔄 Reset Contadores"):
            st.session_state.assistant.session_tokens = 0
            st.session_state.assistant.total_tokens = 0
            st.rerun()
    
    # Área principal do chat
    st.header("💬 Chat")
    
    # Mostrar mensagens existentes
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem..."):
        if not api_key:
            st.error("Por favor, configure sua API Key OpenAI na sidebar")
            return
        
        # Adicionar mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mostrar mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Processar arquivo se enviado
        file_content = None
        file_info = None
        if uploaded_file:
            file_content = st.session_state.assistant.process_file(uploaded_file)
            file_info = f"Arquivo: {uploaded_file.name} ({uploaded_file.size} bytes)"
            st.info(f"Arquivo processado: {uploaded_file.name}")
        
        # Gerenciar contexto
        managed_messages = st.session_state.assistant.manage_context_window(
            st.session_state.messages, max_context_messages
        )
        
        # Obter resposta do assistente
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                model_name = st.session_state.assistant.models[selected_model]
                response = st.session_state.assistant.send_message(
                    managed_messages, 
                    model_name, 
                    file_content,
                    temperature
                )
                
                if "error" in response:
                    st.error(f"Erro: {response['error']}")
                else:
                    st.markdown(response["content"])
                    
                    # Adicionar resposta às mensagens
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": response["content"]
                    })
                    
                    # Log da interação
                    st.session_state.assistant.log_interaction(
                        prompt=prompt,
                        response=response["content"],
                        model=model_name,
                        tokens_used=response["tokens"]["total"],
                        file_info=file_info
                    )
                    
                    # Mostrar informações de tokens
                    st.caption(f"Tokens utilizados - Prompt: {response['tokens']['prompt']}, "
                              f"Resposta: {response['tokens']['completion']}, "
                              f"Total: {response['tokens']['total']}")
    
    # Seção de logs (expansível)
    with st.expander("📋 Logs da Sessão"):
        if os.path.exists("chat_logs.log"):
            with open("chat_logs.log", "r", encoding="utf-8") as f:
                logs = f.read()
            st.code(logs, language="text")
        else:
            st.info("Nenhum log encontrado ainda.")
    
if __name__ == "__main__":
    main()