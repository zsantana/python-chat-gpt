import re
from pathlib import Path

class ArtefatoSplitterSpringBoot:
    def __init__(self, pacote_base="com.example.projeto", pasta_saida="src/main/java"):
        self.pacote_base = pacote_base
        self.pasta_saida = Path(pasta_saida) / Path(*pacote_base.split('.'))

    def split(self, texto):
        blocos = self._extrair_blocos(texto)
        self._salvar_artefatos(blocos)

    def _limpar_nome(self, texto):
        return re.sub(r'\W+', '_', texto.strip()).lower()

    def _extrair_blocos(self, texto):
        blocos = []
        secoes = re.split(r'(?:^|\n)### (.*?)\n', texto)

        for i in range(1, len(secoes), 2):
            titulo = secoes[i].strip()
            conteudo = secoes[i + 1]

            blocos_codigo = re.findall(r'```(?:\w+)?\n(.*?)```', conteudo, re.DOTALL)
            for idx, bloco in enumerate(blocos_codigo):
                blocos.append({
                    "titulo": titulo,
                    "indice": idx,
                    "codigo": bloco.strip()
                })

        return blocos

    def _detectar_subpacote(self, titulo):
        titulo_lower = titulo.lower()
        if "domínio" in titulo_lower or "modelo" in titulo_lower:
            return "domain/model"
        elif "aplicação" in titulo_lower or "service" in titulo_lower:
            return "application/service"
        elif "infraestrutura" in titulo_lower or "repository" in titulo_lower:
            return "infrastructure/repository"
        elif "apresentação" in titulo_lower or "controller" in titulo_lower:
            return "presentation/controller"
        elif "configuração" in titulo_lower:
            return "infrastructure/config"
        else:
            return "shared"

    def _detectar_extensao(self, codigo):
        if "<project" in codigo and "<dependencies>" in codigo:
            return "xml"
        return "java" if "class " in codigo or "interface " in codigo or "@" in codigo else "txt"

    def _gerar_caminho_arquivo(self, bloco):
        subpacote = self._detectar_subpacote(bloco["titulo"])
        extensao = self._detectar_extensao(bloco["codigo"])
        nome_base = self._limpar_nome(bloco["titulo"])
        nome_arquivo = f"{nome_base}_{bloco['indice'] + 1}.{extensao}"

        if extensao == "xml":
            return Path("src/main/resources") / nome_arquivo

        return self.pasta_saida / Path(subpacote) / nome_arquivo

    def _salvar_artefatos(self, blocos):
        for bloco in blocos:
            caminho_arquivo = self._gerar_caminho_arquivo(bloco)
            caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(bloco["codigo"])

            print(f"[✔] Artefato salvo: {caminho_arquivo}")
