from datetime import date, datetime

from control.veiculo_controller import VeiculoController
from model.LocacaoStrategy import CalculoPadraoStrategy, CalculoVIPStrategy
from model.locacao import Locacao, StatusLocacao
from model.veiculo import Categoria


class LocacaoController:
    _locacoes = []
    _proximo_id = 1

    def __init__(self):
        self.veiculo_controller = VeiculoController()

    @staticmethod
    def _parse_data(valor):
        if isinstance(valor, date):
            return valor
        return datetime.strptime(valor.strip(), "%Y-%m-%d").date()

    @staticmethod
    def _parse_status(valor):
        if isinstance(valor, StatusLocacao):
            return valor
        return StatusLocacao(str(valor).strip().lower())

    @staticmethod
    def _parse_categoria(valor):
        if not valor or valor == "TODAS":
            return None
        if isinstance(valor, Categoria):
            return valor
        return Categoria[str(valor).strip().upper()]

    @staticmethod
    def _parse_estrategia(valor):
        if str(valor).strip().upper() == "VIP":
            return CalculoVIPStrategy()
        return CalculoPadraoStrategy()

    @staticmethod
    def _nome_estrategia(locacao):
        if isinstance(locacao.estrategia, CalculoVIPStrategy):
            return "VIP"
        return "PADRAO"

    @staticmethod
    def _periodos_sobrepostos(inicio_a, fim_a, inicio_b, fim_b):
        fim_a = fim_a or inicio_a
        fim_b = fim_b or inicio_b
        return inicio_a <= fim_b and inicio_b <= fim_a

    def listar_locacoes(self):
        return list(self._locacoes)

    def buscar_por_id(self, id_locacao):
        return next((l for l in self._locacoes if l.id == int(id_locacao)), None)

    def buscar_veiculos_disponiveis(self, data_inicio, data_fim, categoria="TODAS"):
        inicio = self._parse_data(data_inicio)
        fim = self._parse_data(data_fim)
        categoria_enum = self._parse_categoria(categoria)

        if inicio > fim:
            raise ValueError("Data de inicio deve ser anterior ou igual a data de fim.")

        veiculos = self.veiculo_controller.listar_veiculos()
        disponiveis = []

        for veiculo in veiculos:
            if categoria_enum is not None and veiculo.categoria != categoria_enum:
                continue

            ocupado = any(
                locacao.veiculo.placa == veiculo.placa
                and locacao.status in (StatusLocacao.RESERVADO, StatusLocacao.LOCADO)
                and self._periodos_sobrepostos(inicio, fim, locacao.data_inicio, locacao.data_fim)
                for locacao in self._locacoes
            )
            if not ocupado:
                disponiveis.append(veiculo)

        return disponiveis

    def criar_locacao(
        self,
        placa,
        data_inicio,
        data_fim,
        status="reservado",
        estrategia_nome="PADRAO",
        validar_disponibilidade=True,
    ):
        try:
            inicio = self._parse_data(data_inicio)
            fim = self._parse_data(data_fim)
            status_enum = self._parse_status(status)
            estrategia = self._parse_estrategia(estrategia_nome)
            veiculo = self.veiculo_controller.buscar_por_placa(placa)

            if veiculo is None:
                return False, "Veiculo nao encontrado."
            if inicio > fim:
                return False, "Data de inicio deve ser anterior ou igual a data de fim."
            if validar_disponibilidade:
                disponiveis = self.buscar_veiculos_disponiveis(inicio, fim, veiculo.categoria)
                if not any(v.placa == veiculo.placa for v in disponiveis):
                    return False, "Veiculo indisponivel no periodo informado."

            locacao = Locacao(veiculo, inicio, fim, estrategia, status_enum)
            locacao.id = self._proximo_id
            self.__class__._proximo_id += 1
            self._locacoes.append(locacao)
            return True, "Locacao cadastrada com sucesso."

        except Exception as erro:
            return False, f"Erro ao cadastrar locacao: {erro}"

    def atualizar_locacao(self, id_locacao, placa, data_inicio, data_fim, status, estrategia_nome):
        locacao = self.buscar_por_id(id_locacao)
        if locacao is None:
            return False, "Locacao nao encontrada."

        try:
            inicio = self._parse_data(data_inicio)
            fim = self._parse_data(data_fim)
            veiculo = self.veiculo_controller.buscar_por_placa(placa)
            if veiculo is None:
                return False, "Veiculo nao encontrado."
            if inicio > fim:
                return False, "Data de inicio deve ser anterior ou igual a data de fim."

            locacao.veiculo = veiculo
            locacao.data_inicio = inicio
            locacao.data_fim = fim
            locacao.status = self._parse_status(status)
            locacao.estrategia = self._parse_estrategia(estrategia_nome)
            return True, "Locacao atualizada com sucesso."

        except Exception as erro:
            return False, f"Erro ao atualizar locacao: {erro}"

    def remover_locacao(self, id_locacao):
        locacao = self.buscar_por_id(id_locacao)
        if locacao is None:
            return False, "Locacao nao encontrada."
        self._locacoes.remove(locacao)
        return True, "Locacao removida com sucesso."

    def locar(self, id_locacao):
        locacao = self.buscar_por_id(id_locacao)
        if locacao is None:
            return False, "Locacao nao encontrada."
        if locacao.status != StatusLocacao.RESERVADO:
            return False, "Somente reservas podem ser locadas."

        hoje = date.today()
        if locacao.data_inicio != hoje:
            locacao.data_inicio = hoje
            if locacao.data_fim is not None and locacao.data_fim < hoje:
                locacao.data_fim = hoje

        locacao.status = StatusLocacao.LOCADO
        return True, "Locacao marcada como locada."

    def devolver(self, id_locacao):
        locacao = self.buscar_por_id(id_locacao)
        if locacao is None:
            return False, "Locacao nao encontrada."
        if locacao.status != StatusLocacao.LOCADO:
            return False, "Somente locacoes com status locado podem ser devolvidas."

        hoje = date.today()
        if locacao.data_inicio >= hoje:
            return False, "A data de inicio deve ser anterior a data atual para devolucao."

        locacao.data_fim = hoje
        locacao.status = StatusLocacao.DEVOLVIDO
        return True, self.detalhes_locacao(locacao.id)

    def cancelar(self, id_locacao):
        locacao = self.buscar_por_id(id_locacao)
        if locacao is None:
            return False, "Locacao nao encontrada."
        if locacao.status != StatusLocacao.RESERVADO:
            return False, "Somente reservas podem ser canceladas."

        locacao.status = StatusLocacao.CANCELADO
        return True, "Reserva cancelada com sucesso."

    def detalhes_locacao(self, id_locacao):
        locacao = self.buscar_por_id(id_locacao)
        if locacao is None:
            return "Locacao nao encontrada."

        linhas = [
            f"Codigo: {locacao.id}",
            f"Veiculo: {locacao.veiculo.placa} ({locacao.veiculo.__class__.__name__})",
            f"Categoria: {locacao.veiculo.categoria.name}",
            f"Status: {locacao.status.value}",
            f"Estrategia: {self._nome_estrategia(locacao)}",
        ]

        if locacao.status == StatusLocacao.CANCELADO:
            linhas.append("Locacao cancelada. Valor nao calculado.")
            return "\n".join(linhas)

        linhas.append(f"Data de inicio: {locacao.data_inicio.strftime('%Y-%m-%d')}")
        if locacao.status == StatusLocacao.DEVOLVIDO:
            linhas.append(f"Data de devolucao: {locacao.data_fim.strftime('%Y-%m-%d')}")
            linhas.append(f"Numero de diarias: {locacao.quantidade_diarias()}")
            linhas.append(f"Valor total: R$ {locacao.calcular_valor_locacao():.2f}")
        else:
            linhas.append(f"Data de fim prevista: {locacao.data_fim.strftime('%Y-%m-%d')}")
            linhas.append(f"Valor estimado: R$ {locacao.calcular_valor_locacao():.2f}")

        return "\n".join(linhas)

    def nome_estrategia(self, locacao):
        return self._nome_estrategia(locacao)
