import json
from core.logger import registrar_erro
from core.pipeline import PipelineDados
from core.produtos import CatalogoProdutos
from core.llm import ClienteLLM
from core.models import Negociacao
from core.enums import StatusNegociacao
from core.config import PROMPT_PRINCIPAL, PROMPT_CLASSIFICADOR, MATRIZ_OBJECOES

class AgenteFyz:
    def __init__(self):
        self.llm = ClienteLLM()
        self.catalogo = CatalogoProdutos()
        self.resumo_conversa = []
        self.dados_venda = Negociacao()

    def _carregar_prompt(self, caminho):
        try:
            with open(caminho, "r", encoding="utf-8") as f: return f.read()
        except Exception as e:
            registrar_erro("ERRO_LEITURA", str(e))
            return ""

    def iniciar(self):
        print("="*60)
        print(f"🤖 Agente Fyz B2B | {self.llm.modelo}")
        print("="*60)
        self._fluxo_consultor()

    def _fluxo_consultor(self):
        # Instrução inicial
        instrucao = (
            f"{self._carregar_prompt(PROMPT_PRINCIPAL)}\n"
            f"OBJEÇÕES:\n{self._carregar_prompt(MATRIZ_OBJECOES)}\n"
            "REGRA OBRIGATÓRIA: Use a tag [FIM_PEDIDO] ao concluir a negociação."
        )
        
        chat = self.llm.iniciar_chat(instrucao)

        while True:
            msg = input("\nDono da Padaria: ")
            if msg.lower() in ['sair', 'quit', 'exit']: 
                self.dados_venda.status_negociacao = StatusNegociacao.CANCELADO
                break
            
            # Salva cliente no banco
            PipelineDados.salvar_mensagem_bd(self.dados_venda.id_negociacao, self.dados_venda.telefone_cliente, "cliente", msg)
            self.resumo_conversa.append(f"Cliente: {msg}")

            # RAG
            contexto_produto = self.catalogo.buscar_contexto(msg)
            msg_ia = (
                f"DADOS TÉCNICOS PARA VENDA:\n{contexto_produto}\n\n"
                "INSTRUÇÃO: Use estes dados para vender. Seja direto e objetivo.\n\n"
                f"Cliente: {msg}"
            ) if len(contexto_produto) > 50 else msg

            sucesso, resposta = self.llm.enviar_mensagem_com_retry(chat, msg_ia)
            if not sucesso: break
            
            texto_limpo = resposta.replace("[FIM_PEDIDO]", "").strip()
            print(f"\nAgente Fiz: {texto_limpo}")
            print("-" * 60)
            
            # Salva IA no banco
            PipelineDados.salvar_mensagem_bd(self.dados_venda.id_negociacao, self.dados_venda.telefone_cliente, "agente", texto_limpo)
            self.resumo_conversa.append(f"Agente: {texto_limpo}")

            if "[FIM_PEDIDO]" in resposta:
                print("\n[Sistema]: Venda concluída. Extraindo dados...")
                self._extrair_inteligencia()
                break

    def _extrair_inteligencia(self):
        prompt_classificador = self._carregar_prompt(PROMPT_CLASSIFICADOR)
        historico = "\n".join(self.resumo_conversa)
        
        sucesso, resposta_json = self.llm.extrair_json_com_retry(prompt_classificador, historico)
        if sucesso:
            try:
                dados_extraidos = json.loads(resposta_json.strip())
                for chave, valor in dados_extraidos.items():
                    if hasattr(self.dados_venda, chave):
                        if chave == "status_negociacao":
                            try: setattr(self.dados_venda, chave, StatusNegociacao(valor))
                            except ValueError: pass
                        else:
                            setattr(self.dados_venda, chave, valor)
            except Exception as e:
                registrar_erro("FALHA_CONVERSAO_JSON", str(e))
        
        self._salvar_dados()

    def _salvar_dados(self):
        PipelineDados.salvar_negociacao(self.dados_venda)
        print("\n✅ Sucesso! Tabelas 'mensagens', 'negociacoes' e 'clientes' atualizadas no SQLite.")