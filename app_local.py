import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# ==========================================================
# 1. CARREGAR VARIÁVEIS DE AMBIENTE
# ==========================================================
load_dotenv()
API_KEY = os.getenv("API_KEY_LLM")

if not API_KEY:
    print("❌ ERRO: Chave de API não encontrada.")
    print("Crie um arquivo .env com:")
    print("API_KEY_LLM=sua_chave_aqui")
    exit()

genai.configure(api_key=API_KEY)


# ==========================================================
# FUNÇÃO PARA LER ARQUIVOS
# ==========================================================
def carregar_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f"⚠️ Arquivo não encontrado: {caminho_arquivo}")
        return ""


# ==========================================================
# CARREGAR BASE DE CONHECIMENTO
# ==========================================================
prompt_principal = carregar_arquivo("prompts/prompt-principal.md")
catalogo_produtos = carregar_arquivo("knowledge/produtos-fiz.md")
objecoes = carregar_arquivo("knowledge/matriz-objecoes.md")
prompt_classificador = carregar_arquivo("prompts/prompt-classificador.md")


instrucao_sistema = f"""
{prompt_principal}

BASE DE CONHECIMENTO (PRODUTOS):
{catalogo_produtos}

COMO CONTORNAR OBJEÇÕES:
{objecoes}
"""


# ==========================================================
# MODELO DE VENDAS
# ==========================================================
modelo_vendas = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=instrucao_sistema,
    generation_config={
        "temperature": 0.7,
        "top_p": 0.9,
        "max_output_tokens": 1000
    }
)


# ==========================================================
# MODELO CLASSIFICADOR
# ==========================================================
modelo_classificador = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=prompt_classificador,
    generation_config={
        "temperature": 0.1,
        "max_output_tokens": 1000
    }
)


# ==========================================================
# INICIAR CHAT
# ==========================================================
chat = modelo_vendas.start_chat(history=[])


# ==========================================================
# INTERFACE
# ==========================================================
print("=" * 60)
print("🤖 Agente Fiz B2B Inicializado!")
print("Digite 'sair' para encerrar.")
print("=" * 60)


while True:

    mensagem_usuario = input("\nDono da Padaria: ")

    if mensagem_usuario.lower() in ["sair", "exit", "quit"]:

        print("\nEncerrando o Agente Fiz. Boas vendas!")

        # =============================================
        # HISTÓRICO COMPLETO
        # =============================================
        historico_completo = "\n".join(
            [f"{m.role}: {m.parts[0].text}" for m in chat.history]
        )

        print("\n📊 Extraindo dados da negociação...")

        try:

            prompt_dashboard = f"""
Analise a conversa abaixo e responda SOMENTE um JSON válido.

Conversa:
{historico_completo}

Retorne no formato:

{{
    "nome_cliente": "",
    "telefone": "",
    "cidade": "",
    "produto_interesse": "",
    "quantidade": "",
    "nivel_interesse": "",
    "objecoes": [],
    "status_negociacao": "",
    "resumo": ""
}}

Não escreva explicações.
Não use markdown.
Não coloque ```json.
Retorne apenas JSON puro.
"""

            resposta_dashboard = modelo_classificador.generate_content(
                prompt_dashboard
            )

            texto_json = resposta_dashboard.text.strip()

            # Remove possíveis marcações ```json
            texto_json = texto_json.replace("```json", "")
            texto_json = texto_json.replace("```", "")
            texto_json = texto_json.strip()

            dados = json.loads(texto_json)

            print("\n📊 Dados extraídos:")
            print(json.dumps(dados, indent=4, ensure_ascii=False))

            # Salvar em arquivo
            with open(
                "dashboard.json",
                "w",
                encoding="utf-8"
            ) as arquivo:

                json.dump(
                    dados,
                    arquivo,
                    ensure_ascii=False,
                    indent=4
                )

            print("\n✅ dashboard.json salvo com sucesso.")

        except Exception as e:

            print("\n❌ Erro ao gerar JSON.")
            print(e)

            try:
                print("\nResposta bruta recebida:")
                print(resposta_dashboard.text)
            except:
                pass

        break

    # ==================================================
    # CHAT DE VENDAS
    # ==================================================
    try:

        resposta_vendas = chat.send_message(mensagem_usuario)

        print(f"\nAgente Fiz: {resposta_vendas.text}")
        print("-" * 60)

    except Exception as e:

        print("\n❌ Erro de comunicação com a API:")
        print(e)