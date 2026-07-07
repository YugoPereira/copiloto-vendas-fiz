import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_LLM = os.getenv("API_KEY_LLM")
MODELO_LLM = "gemini-2.5-flash"

# Caminhos dos arquivos
PROMPT_PRINCIPAL = "prompts/prompt-principal.md"
PROMPT_CLASSIFICADOR = "prompts/prompt-classificador.md"
MATRIZ_OBJECOES = "knowledge/matriz-objecoes.md"
CATALOGO_PRODUTOS = "knowledge/produtos-fyz.json"

# Pastas de saída
DIR_DASHBOARDS = "dashboards"
DIR_HISTORICO = "historico"
DIR_DATASETS = "datasets"
DIR_LOGS = "logs"
DIR_DATABASE = "database" # Nossa nova casa para o SQLite