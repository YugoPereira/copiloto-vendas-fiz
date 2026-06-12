import json
from core.logger import registrar_erro
from core.config import CATALOGO_PRODUTOS

class CatalogoProdutos:
    def __init__(self):
        try:
            with open(CATALOGO_PRODUTOS, "r", encoding="utf-8") as f:
                self.produtos = json.load(f)
        except Exception as e:
            registrar_erro("ARQUIVO_PRODUTOS", str(e))
            self.produtos = {}

    def buscar_contexto(self, mensagem_cliente):
        mensagem_lower = mensagem_cliente.lower()
        for chave, dados in self.produtos.items():
            nome_limpo = chave.replace("_", " ")
            if nome_limpo in mensagem_lower or dados["nome"].lower() in mensagem_lower:
                return json.dumps({chave: dados}, ensure_ascii=False)
        return json.dumps(self.produtos, ensure_ascii=False)