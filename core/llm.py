import time
from google import genai
from google.genai import types
from core.config import API_KEY_LLM, MODELO_LLM
from core.logger import registrar_erro

class ClienteLLM:
    def __init__(self):
        if not API_KEY_LLM:
            raise ValueError("Chave de API não encontrada.")
        self.client = genai.Client(api_key=API_KEY_LLM)
        self.modelo = MODELO_LLM

    def iniciar_chat(self, instrucao):
        # 🌟 Aumentado para 500: Dá fôlego de sobra para a IA responder sem ser cortada
        config = types.GenerateContentConfig(
            system_instruction=instrucao, 
            temperature=0.3, 
            max_output_tokens=500
        )
        return self.client.chats.create(model=self.modelo, config=config)

    def enviar_mensagem_com_retry(self, chat, mensagem, tentativas=3):
        """Implementa o Exponential Backoff 10s, 20s, 40s"""
        for tentativa in range(tentativas):
            try:
                res = chat.send_message(mensagem)
                return True, res.text
            except Exception as e:
                if "429" in str(e):
                    espera = (2 ** tentativa) * 10
                    print(f"⚠️ Limite API. Aguardando {espera}s...")
                    time.sleep(espera)
                else:
                    registrar_erro("API_CHAT", str(e))
                    return False, ""
        return False, ""

    def extrair_json_com_retry(self, instrucao, conteudo, tentativas=3):
        # 🌟 Adicionado max_output_tokens=1000: Garante que o JSON não será quebrado
        config = types.GenerateContentConfig(
            system_instruction=instrucao, 
            temperature=0.0, 
            max_output_tokens=1000, 
            response_mime_type="application/json"
        )
        for tentativa in range(tentativas):
            try:
                res = self.client.models.generate_content(model=self.modelo, contents=conteudo, config=config)
                return True, res.text
            except Exception as e:
                if "429" in str(e):
                    time.sleep((2 ** tentativa) * 10)
                else:
                    registrar_erro("API_EXTRACAO", str(e))
        return False, ""