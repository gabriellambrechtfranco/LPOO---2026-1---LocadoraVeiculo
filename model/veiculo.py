from abc import ABC
from enum import Enum

from .ExcecoesPersonalizadas import PlacaInvalidaError
from .estados_veiculo import DisponivelState


class Categoria(Enum):
    ECONOMICO = "ECONOMICO"
    EXECUTIVO = "EXECUTIVO"


class Veiculo(ABC):
    def __init__(self, placa: str, taxa_diaria: float, categoria: Categoria = Categoria.ECONOMICO):
        self.__placa = ""
        self.__taxa_diaria = 0.0
        self._estado_atual = None
        self.placa = placa
        self.categoria = categoria
        self.taxa_diaria = taxa_diaria
        self.estado_atual = DisponivelState(self)

    @property
    def estado_atual(self):
        return self._estado_atual

    @estado_atual.setter
    def estado_atual(self, novo_estado):
        self._estado_atual = novo_estado

    def tentar_alugar(self):
        self.estado_atual.alugar()

    def tentar_devolver(self):
        self.estado_atual.devolver()

    def reter_na_frota_pra_conserto(self):
        self.estado_atual.enviar_manutencao()

    def exibir_dados(self):
        estado = self.estado_atual.__class__.__name__.strip().lower().replace("state", "")
        return (
            f"Placa: {self.placa}\n"
            f"Categoria: {self.categoria.name}\n"
            f"Taxa Diaria: R$ {self.taxa_diaria:.2f}\n"
            f"Estado: {estado}"
        )

    @property
    def placa(self):
        return self.__placa

    @placa.setter
    def placa(self, placa):
        if self.valida_placa(placa):
            self.__placa = placa.strip().replace("-", "").upper()

    @property
    def taxa_diaria(self):
        return self.__taxa_diaria

    @taxa_diaria.setter
    def taxa_diaria(self, taxa_diaria: float):
        if taxa_diaria is None:
            raise ValueError("A taxa diaria e obrigatoria!")
        if taxa_diaria < 0:
            raise ValueError("A taxa diaria do veiculo deve ser maior que zero.")
        self.__taxa_diaria = taxa_diaria

    def valida_placa(self, placa: str):
        placa = placa.strip().replace("-", "").upper()
        if len(placa) != 7:
            raise PlacaInvalidaError("Placa invalida! Placa deve conter 7 caracteres")
        if not placa[0:3].isalpha():
            raise PlacaInvalidaError("Placa invalida! Os primeiros 3 caracteres devem ser letras")
        if not placa[3].isdigit() or not placa[5:7].isdigit():
            raise PlacaInvalidaError("Placa invalida! O 4o, 6o e 7o caracteres devem ser numeros")
        if not placa[4].isalnum():
            raise PlacaInvalidaError("Placa invalida! O 5o caracter deve ser uma letra ou numero")
        return True


class Carro(Veiculo):
    def __init__(self, placa: str, taxa_diaria: float, categoria: Categoria = Categoria.ECONOMICO):
        super().__init__(placa, taxa_diaria, categoria=categoria)
        self.valor_seguro = 50


class Motorhome(Veiculo):
    def __init__(self, placa: str, taxa_diaria: float = 0.0, categoria: Categoria = Categoria.ECONOMICO):
        super().__init__(placa, taxa_diaria, categoria=categoria)
        self.valor_seguro = 120


class VeiculoFactory:
    @staticmethod
    def criar_veiculo(tipo: str, placa: str, categoria: Categoria, taxa_diaria: float = 0.0):
        tipo_normalizado = tipo.strip().lower()
        if tipo_normalizado == "carro":
            return Carro(placa, taxa_diaria, categoria)
        if tipo_normalizado == "motorhome":
            return Motorhome(placa, taxa_diaria, categoria)
        raise ValueError(f"Tipo de veiculo invalido: {tipo}. Use 'carro' ou 'motorhome'.")
