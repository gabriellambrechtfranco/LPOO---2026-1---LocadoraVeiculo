from model.veiculo import VeiculoFactory, Categoria

class VeiculoRepository:
    def __init__(self):
        self.veiculos = []

    def listar(self):
        return self.veiculos

    def adicionar(self, tipo, placa, categoria, taxa):
        veiculo = VeiculoFactory.criar_veiculo(
            tipo, placa, categoria, taxa
        )
        self.veiculos.append(veiculo)

    def remover(self, placa):
        self.veiculos = [v for v in self.veiculos if v.placa != placa]