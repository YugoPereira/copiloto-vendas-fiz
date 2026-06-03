import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Carregar Variáveis de Ambiente (Segurança)
# Puxa a chave do arquivo .env sem expor no código-fonte
load_dotenv()
API_KEY = os.getenv("API_KEY_LLM")

if not API_KEY:
    print("❌ ERRO: Chave de API não encontrada. Crie o arquivo .env com a sua API_KEY_LLM.")
    exit()

# Configurar a biblioteca do Gemini com a chave segura
genai.configure(api_key=API_KEY)

# 2. Função para carregar a Base de Conhecimento e Prompts
def carregar_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        print(f"⚠️ Aviso: Arquivo {caminho_arquivo} não encontrado.")
        return ""

# 3. Montar o "Cérebro" do Agente (System Instruction)
prompt_principal = carregar_arquivo("prompts/prompt-principal.md")
catalogo_produtos = carregar_arquivo("knowledge/produtos-fiz.md")
objecoes = carregar_arquivo("knowledge/matriz-objecoes.md")

instrucao_sistema = f"""
{prompt_principal}

BASE DE CONHECIMENTO (PRODUTOS):
{catalogo_produtos}

COMO CONTORNAR OBJEÇÕES:
{objecoes}
"""

# 4. Inicializar o Modelo de IA
# Usamos o gemini-1.5-flash por ser rápido e ideal para chat
modelo = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=instrucao_sistema
)

# Iniciar histórico de conversa vazio
chat = modelo.start_chat(history=[])

# 5. Interface de Terminal (Loop de Interação)
print("="*60)
print("🤖 Agente Fiz B2B Inicializado!")
print("Dica: Digite 'sair' a qualquer momento para encerrar.")
print("="*60)

while True:
    # Captura a mensagem do usuário (simulando o Dono da Padaria)
    mensagem_usuario = input("\nDono da Padaria: ")
    
    # Condição de parada
    if mensagem_usuario.lower() in ['sair', 'exit', 'quit']:
        print("\nEncerrando o Agente Fiz. Boas vendas!")
        break
    
    try:
        # Envia a mensagem para a IA e aguarda a resposta
        resposta = chat.send_message(mensagem_usuario)
        print(f"\nAgente Fiz: {resposta.text}")
        print("-" * 60)
    except Exception as e:
        print(f"\n❌ Erro de comunicação com a API: {e}")