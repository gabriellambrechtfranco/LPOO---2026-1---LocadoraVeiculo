from abc import ABC, abstractmethod


class VeiculoState(ABC):
    def __init__(self, veiculo):
        self.veiculo = veiculo

    @property
    def veiculo(self):
        return self.__veiculo

    @veiculo.setter
    def veiculo(self, valor):
        self.__veiculo = valor

    @abstractmethod
    def alugar(self):
        pass

    @abstractmethod
    def devolver(self):
        pass

    @abstractmethod
    def enviar_manutencao(self):
        pass


class DisponivelState(VeiculoState):
    def alugar(self):
        print(f"Sucesso! O veiculo {self.veiculo.placa} agora esta alugado para um cliente.")
        self.veiculo.estado_atual = AlugadoState(self.veiculo)

    def devolver(self):
        print("Erro: O veiculo ja consta no patio e esta aguardando clientes, nao cabe devolucao.")

    def enviar_manutencao(self):
        print(f"O veiculo {self.veiculo.placa} foi retido no patio da frota para reparos tecnicos.")
        self.veiculo.estado_atual = ManutencaoState(self.veiculo)


class AlugadoState(VeiculoState):
    def alugar(self):
        print(f"Reserva negada. O veiculo {self.veiculo.placa} ja esta sob locacao ativa de outro cliente.")

    def devolver(self):
        print(f"Devolucao registrada. O veiculo {self.veiculo.placa} retorna ao patio.")
        self.veiculo.estado_atual = DisponivelState(self.veiculo)

    def enviar_manutencao(self):
        print("Erro operacional: O carro esta na rua com um cliente, impossivel fazer manutencao agora.")


class ManutencaoState(VeiculoState):
    def alugar(self):
        print(f"Restricao ativa: O veiculo {self.veiculo.placa} nao esta apto a rodagem.")

    def devolver(self):
        print("Fim do periodo de reparos. Lavagem concluida. O carro agora esta disponibilizado.")
        self.veiculo.estado_atual = DisponivelState(self.veiculo)

    def enviar_manutencao(self):
        print("O veiculo ja se encontra nos estaleiros da oficina no momento.")
