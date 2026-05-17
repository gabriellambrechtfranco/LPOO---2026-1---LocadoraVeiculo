from model.veiculo import Categoria, VeiculoFactory


class VeiculoController:
    _veiculos = []
    _dados_iniciais_carregados = False

    def __init__(self):
        self._carregar_dados_iniciais()

    @classmethod
    def _carregar_dados_iniciais(cls):
        if cls._dados_iniciais_carregados:
            return

        cls._veiculos = [
            VeiculoFactory.criar_veiculo("carro", "ABC1D23", Categoria.ECONOMICO, 150.0),
            VeiculoFactory.criar_veiculo("motorhome", "XYZ9A99", Categoria.EXECUTIVO, 300.0),
        ]
        cls._dados_iniciais_carregados = True

    @staticmethod
    def _normalizar_placa(placa: str):
        return placa.strip().replace("-", "").upper()

    @staticmethod
    def _converter_taxa(taxa_str: str):
        taxa_num = float(taxa_str.replace(",", "."))
        if taxa_num <= 0:
            raise ValueError("A taxa diaria deve ser um valor positivo")
        return taxa_num

    @staticmethod
    def _converter_categoria(categoria_str: str):
        return Categoria[categoria_str.upper()]

    def salvar_veiculo(self, placa: str, tipo_str: str, categoria_str: str, taxa_str: str):
        if not placa or not tipo_str or not categoria_str or not taxa_str:
            return False, "Preencha todos os campos"

        try:
            placa_normalizada = self._normalizar_placa(placa)
            if self.buscar_por_placa(placa_normalizada):
                return False, f"Veiculo com placa {placa_normalizada} ja esta cadastrado"

            categoria_enum = self._converter_categoria(categoria_str)
            taxa_num = self._converter_taxa(taxa_str)
            novo_veiculo = VeiculoFactory.criar_veiculo(
                tipo_str.strip().lower(),
                placa_normalizada,
                categoria_enum,
                taxa_num,
            )
            self._veiculos.append(novo_veiculo)
            return True, "Veiculo cadastrado com sucesso"

        except KeyError:
            return False, "Categoria invalida. Use ECONOMICO ou EXECUTIVO"
        except ValueError as erro:
            return False, f"Valor invalido. Erro: {erro}"
        except Exception as erro:
            return False, f"Erro inesperado: {erro}"

    def listar_veiculos(self):
        return list(self._veiculos)

    def buscar_por_placa(self, placa: str):
        placa_normalizada = self._normalizar_placa(placa)
        return next((v for v in self._veiculos if v.placa == placa_normalizada), None)

<<<<<<< Updated upstream
        except Exception as e:
            print(f"Erro ao buscar veículo: {e}")
            return None      
=======
    def remover_veiculo(self, placa: str):
        if not placa:
            return False, "Placa nao informada"

        veiculo = self.buscar_por_placa(placa)
        if not veiculo:
            return False, f"Veiculo com placa {placa} nao foi encontrado"

        self._veiculos.remove(veiculo)
        return True, "Veiculo removido com sucesso"

    def atualizar_veiculo(self, placa: str, tipo_str: str, categoria_str: str, taxa_str: str):
        if not placa or not tipo_str or not categoria_str or not taxa_str:
            return False, "Preencha todos os campos"

        veiculo_existente = self.buscar_por_placa(placa)
        if not veiculo_existente:
            return False, f"Veiculo com placa {placa} nao foi encontrado"

        try:
            categoria_enum = self._converter_categoria(categoria_str)
            taxa_num = self._converter_taxa(taxa_str)
            veiculo_atualizado = VeiculoFactory.criar_veiculo(
                tipo_str.strip().lower(),
                veiculo_existente.placa,
                categoria_enum,
                taxa_num,
            )
            indice = self._veiculos.index(veiculo_existente)
            self._veiculos[indice] = veiculo_atualizado
            return True, "Veiculo atualizado com sucesso"

        except KeyError:
            return False, "Categoria invalida. Use ECONOMICO ou EXECUTIVO"
        except ValueError as erro:
            return False, f"Valor invalido. Erro: {erro}"
        except Exception as erro:
            return False, f"Erro inesperado: {erro}"
>>>>>>> Stashed changes
