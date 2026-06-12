from dataclasses import dataclass, asdict
from datetime import datetime, UTC
import uuid
from core.enums import StatusNegociacao

@dataclass
class Negociacao:
    id_negociacao: str = ""
    telefone_cliente: str = "34999999999" # Simulação do WhatsApp
    nome_cliente: str = ""
    cidade: str = "" # 🌟 ADICIONADO PARA SUPORTAR QUALQUER CIDADE DINAMICAMENTE
    produto_interesse: str = ""
    quantidade: str = ""
    dia_entrega: str = ""
    objecao_principal: str = "Nenhuma"
    status_negociacao: StatusNegociacao = StatusNegociacao.EM_ANDAMENTO
    resumo: str = "Atendimento não finalizado."
    timestamp_inicio: str = ""

    def __post_init__(self):
        if not self.id_negociacao:
            self.id_negociacao = str(uuid.uuid4())[:8]
        if not self.timestamp_inicio:
            self.timestamp_inicio = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        d = asdict(self)
        d['status_negociacao'] = self.status_negociacao.value
        return d