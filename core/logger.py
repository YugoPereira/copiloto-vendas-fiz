import os
from datetime import datetime
from core.config import DIR_LOGS

def registrar_erro(tipo_erro, mensagem):
    os.makedirs(DIR_LOGS, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{DIR_LOGS}/erros.log", "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {tipo_erro}: {mensagem}\n")