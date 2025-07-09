import re
from pathlib import Path

class ArtefatoSplitterSpringBoot:
    def __init__(self, pasta_raiz="artefatos_java/src/main"):
        self.pasta_java = Path(pasta_raiz) / "java"
        self.pasta_resources = Path(pasta_raiz) / "resources"

    def split(self, texto):
        blocos = self._extrair_blocos(texto)
        self._salvar_blocos(blocos)

    def _extrair_blocos(self, texto):
        blocos = []
        secoes = re.split(r'(?:^|\n)### (.*?)\n', texto)

        for i in range(1, len(secoes), 2):
            titulo = secoes[i].strip()
            conteudo = secoes[i + 1]

            blocos_codigo = re.findall(r'```(?:\w+)?\n(.*?)```', conteudo, re.DOTALL)
            for idx, codigo in enumerate(blocos_codigo):
                blocos.append({
                    "titulo": titulo,
                    "indice": idx,
                    "codigo": codigo.strip()
                })
        return blocos

    def _detectar_extensao(self, codigo):
        if "<project" in codigo and "<dependencies>" in codigo:
            return "xml"
        elif codigo.strip().startswith("package ") or "class " in codigo or "interface " in codigo:
            return "java"
        elif "=" in codigo and not codigo.strip().startswith("public "):
            return "properties"
        return "txt"

    def _extrair_package(self, codigo):
        match = re.search(r'^package\s+([\w\.]+);', codigo, re.MULTILINE)
        return match.group(1) if match else None

    def _extrair_nome_classe(self, codigo):
        match = re.search(r'\b(class|interface|record)\s+(\w+)', codigo)
        return match.group(2) if match else "Arquivo"

    def _gerar_caminho_arquivo(self, bloco):
        codigo = bloco["codigo"]
        extensao = self._detectar_extensao(codigo)

        if extensao == "java":
            pacote = self._extrair_package(codigo)
            if not pacote:
                raise ValueError("Arquivo Java sem declaração de package.")
            caminho_pacote = Path(*pacote.split("."))
            nome_arquivo = f"{self._extrair_nome_classe(codigo)}.java"
            return self.pasta_java / caminho_pacote / nome_arquivo

        elif extensao in ["xml", "properties"]:
            nome_base = self._limpar_nome(bloco["titulo"])
            nome_arquivo = f"{nome_base}_{bloco['indice'] + 1}.{extensao}"
            return self.pasta_resources / nome_arquivo

        else:
            nome_base = self._limpar_nome(bloco["titulo"])
            nome_arquivo = f"{nome_base}_{bloco['indice'] + 1}.{extensao}"
            return Path("outros") / nome_arquivo

    def _limpar_nome(self, texto):
        return re.sub(r'\W+', '_', texto.strip()).lower()

    def _salvar_blocos(self, blocos):
        for bloco in blocos:
            caminho_arquivo = self._gerar_caminho_arquivo(bloco)
            caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write(bloco["codigo"])

            print(f"[✔] Arquivo salvo: {caminho_arquivo}")
