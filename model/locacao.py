from datetime import date
from enum import Enum

from .ExcecoesPersonalizadas import DataInvalidaError
from .LocacaoStrategy import CalculoLocacaoStrategy, CalculoPadraoStrategy
from .veiculo import Veiculo


class StatusLocacao(Enum):
    RESERVADO = "reservado"
    LOCADO = "locado"
    DEVOLVIDO = "devolvido"
    CANCELADO = "cancelado"


class Locacao:
    def __init__(
        self,
        veiculo: Veiculo,
        data_inicio: date,
        data_fim: date = None,
        estrategia: CalculoLocacaoStrategy = None,
        status: StatusLocacao = StatusLocacao.RESERVADO,
    ):
        self.id = None
        self.__data_inicio = None
        self.__data_fim = None

        self.veiculo = veiculo
        self.data_inicio = data_inicio
        self.data_fim = data_fim
<<<<<<< Updated upstream
        self.estrategia = estrategia
    
=======
        self.estrategia = estrategia or CalculoPadraoStrategy()
        self.status = status

>>>>>>> Stashed changes
    @property
    def veiculo(self):
        return self.__veiculo

    @veiculo.setter
    def veiculo(self, obj: Veiculo):
        if obj is None:
            raise Exception("Objeto Veiculo obrigatorio.")
        self.__veiculo = obj

    @property
    def data_inicio(self):
        return self.__data_inicio

    @data_inicio.setter
    def data_inicio(self, data_inicio: date):
        if data_inicio is None:
            raise DataInvalidaError("Data de inicio e obrigatoria.")
        if self.data_fim is not None and data_inicio > self.data_fim:
            raise DataInvalidaError("Data de inicio nao pode ser posterior a data de fim.")
        self.__data_inicio = data_inicio

    @property
    def data_fim(self):
        return self.__data_fim

    @data_fim.setter
    def data_fim(self, data_fim: date):
        if data_fim is not None and self.data_inicio is not None and self.data_inicio > data_fim:
            raise DataInvalidaError("Data de inicio nao pode ser posterior a data de fim.")
        self.__data_fim = data_fim

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        if isinstance(status, StatusLocacao):
            self.__status = status
            return
        self.__status = StatusLocacao(str(status).strip().lower())

    def quantidade_diarias(self):
        data_fim = self.data_fim or date.today()
        dias = (data_fim - self.data_inicio).days
        if dias <= 0:
            dias = 1
        return dias

    def calcular_valor_locacao(self) -> float:
        return float(self.estrategia.calcular_diarias(self.veiculo, self.quantidade_diarias()))
