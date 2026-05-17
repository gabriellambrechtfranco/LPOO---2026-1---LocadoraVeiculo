import os
import sys
from datetime import date

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.ExcecoesPersonalizadas import DataInvalidaError
from model.LocacaoStrategy import CalculoVIPStrategy
from model.decoradores import GPSDecorator, SeguroTerceirosDecorator
from model.locacao import Locacao
from model.veiculo import Categoria, VeiculoFactory


print("\n--- TESTANDO FACTORY ---")
carro = VeiculoFactory.criar_veiculo("carro", "ABC1D34", Categoria.ECONOMICO, taxa_diaria=150.0)
motorhome = VeiculoFactory.criar_veiculo("motorhome", "XYZ9A99", Categoria.EXECUTIVO, taxa_diaria=200.0)
print("Veiculos criados com sucesso via Factory.")

try:
    VeiculoFactory.criar_veiculo("moto", "DEF2G56", Categoria.ECONOMICO, taxa_diaria=50.0)
    print("Erro: deveria ter lancado ValueError para tipo invalido.")
except ValueError as erro:
    print(f"Excecao capturada corretamente: {erro}")


print("\n--- TESTANDO STRATEGY ---")
data_in = date(2026, 3, 10)
data_out = date(2026, 3, 15)

locacao_normal = Locacao(veiculo=carro, data_inicio=data_in, data_fim=data_out)
print(f"Valor padrao: R$ {locacao_normal.calcular_valor_locacao()}")

locacao_vip = Locacao(veiculo=carro, data_inicio=data_in, data_fim=data_out, estrategia=CalculoVIPStrategy())
print(f"Valor cliente VIP: R$ {locacao_vip.calcular_valor_locacao()}")

locacao_mesmo_dia = Locacao(veiculo=motorhome, data_inicio=date.today(), data_fim=date.today())
print(f"Valor locacao no mesmo dia: R$ {locacao_mesmo_dia.calcular_valor_locacao()}")

try:
    Locacao(veiculo=carro, data_inicio=date(2026, 3, 5), data_fim=date(2026, 3, 1))
    print("Erro: deveria ter lancado DataInvalidaError para datas invalidas.")
except DataInvalidaError as erro:
    print(f"Excecao capturada corretamente: {erro}")


print("\n--- TESTANDO STATE ---")
carro_estado = VeiculoFactory.criar_veiculo("carro", "HJI3K45", Categoria.ECONOMICO, taxa_diaria=100.0)
carro_estado.tentar_alugar()
carro_estado.tentar_alugar()
carro_estado.reter_na_frota_pra_conserto()
carro_estado.tentar_devolver()
carro_estado.reter_na_frota_pra_conserto()
carro_estado.tentar_alugar()


print("\n--- TESTANDO DECORATOR ---")
locacao_base = Locacao(veiculo=carro, data_inicio=date(2026, 3, 1), data_fim=date(2026, 3, 5))
print(f"Valor base: R$ {locacao_base.calcular_valor_locacao()}")

locacao_com_gps = GPSDecorator(locacao_base)
print(f"Valor com GPS: R$ {locacao_com_gps.calcular_valor_locacao()}")

locacao_completa = SeguroTerceirosDecorator(locacao_com_gps)
print(f"Valor com GPS e seguro terceiros: R$ {locacao_completa.calcular_valor_locacao()}")
