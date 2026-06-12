from enum import Enum

class StatusNegociacao(Enum):
    EM_ANDAMENTO = "Em Andamento"
    PEDIDO_FECHADO = "Pedido Fechado"
    CANCELADO = "Cancelado"
    SEM_INTERESSE = "Sem Interesse"