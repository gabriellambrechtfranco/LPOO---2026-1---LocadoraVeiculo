import tkinter as tk
from tkinter import messagebox, ttk

from control.locacao_controller import LocacaoController
from model.veiculo import Categoria


class JanelaNovaReserva(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = LocacaoController()
        self.title("Nova Reserva")
        self.geometry("430x380")

        tk.Label(self, text="Nova Reserva", font=("Helvetica", 16, "bold")).pack(pady=10)

        self.txt_inicio = self._entrada("Data inicio (YYYY-MM-DD)")
        self.txt_fim = self._entrada("Data fim (YYYY-MM-DD)")
        self.cb_categoria = self._combo("Categoria", ["TODAS"] + [c.name for c in Categoria])
        self.cb_veiculo = self._combo("Veiculo disponivel", [])
        self.cb_estrategia = self._combo("Estrategia", ["PADRAO", "VIP"])

        tk.Button(self, text="Buscar Veiculos", command=self.carregar_disponiveis).pack(pady=(12, 4))
        tk.Button(self, text="Salvar Reserva", command=self.salvar).pack(pady=6)

        self.cb_categoria.current(0)
        self.cb_estrategia.current(0)

    def _entrada(self, texto):
        frame = tk.Frame(self)
        frame.pack(fill="x", padx=24, pady=4)
        tk.Label(frame, text=texto).pack(side="left")
        entrada = tk.Entry(frame)
        entrada.pack(side="right", expand=True, fill="x")
        return entrada

    def _combo(self, texto, valores):
        frame = tk.Frame(self)
        frame.pack(fill="x", padx=24, pady=4)
        tk.Label(frame, text=texto).pack(side="left")
        combo = ttk.Combobox(frame, values=valores, state="readonly")
        combo.pack(side="right", expand=True, fill="x")
        return combo

    def carregar_disponiveis(self):
        try:
            veiculos = self.controller.buscar_veiculos_disponiveis(
                self.txt_inicio.get(),
                self.txt_fim.get(),
                self.cb_categoria.get(),
            )
            placas = [v.placa for v in veiculos]
            self.cb_veiculo["values"] = placas
            if placas:
                self.cb_veiculo.current(0)
            else:
                self.cb_veiculo.set("")
                messagebox.showinfo("Aviso", "Nenhum veiculo disponivel para os filtros.", parent=self)
        except Exception as erro:
            messagebox.showerror("Erro", str(erro), parent=self)

    def salvar(self):
        if not self.cb_veiculo.get():
            messagebox.showwarning("Aviso", "Busque e selecione um veiculo disponivel.", parent=self)
            return

        sucesso, msg = self.controller.criar_locacao(
            self.cb_veiculo.get(),
            self.txt_inicio.get(),
            self.txt_fim.get(),
            "reservado",
            self.cb_estrategia.get(),
            validar_disponibilidade=True,
        )
        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)


class JanelaLocacaoUsuario(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = LocacaoController()
        self.title("Locar Veiculo")
        self.geometry("900x430")
        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        tk.Label(self, text="Locacoes - Usuario da Locadora", font=("Helvetica", 16, "bold")).pack(pady=10)

        colunas = ("ID", "Placa", "Tipo", "Inicio", "Fim", "Status")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        frame = tk.Frame(self)
        frame.pack(fill="x", padx=20, pady=5)
        tk.Button(frame, text="Nova Reserva", width=14, command=self.nova_reserva).pack(side="left", padx=5)
        tk.Button(frame, text="Locar", width=10, command=self.locar).pack(side="left", padx=5)
        tk.Button(frame, text="Devolver", width=10, command=self.devolver).pack(side="left", padx=5)
        tk.Button(frame, text="Cancelar", width=10, command=self.cancelar).pack(side="left", padx=5)
        tk.Button(frame, text="Ver Detalhes", width=14, command=self.ver_detalhes).pack(side="left", padx=5)
        tk.Button(frame, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for locacao in self.controller.listar_locacoes():
            self.tree.insert("", "end", values=(
                locacao.id,
                locacao.veiculo.placa,
                locacao.veiculo.__class__.__name__,
                locacao.data_inicio.strftime("%Y-%m-%d"),
                locacao.data_fim.strftime("%Y-%m-%d"),
                locacao.status.value,
            ))

    def _locacao_selecionada(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma locacao.", parent=self)
            return None
        id_locacao = self.tree.item(selecionado[0])["values"][0]
        return self.controller.buscar_por_id(id_locacao)

    def nova_reserva(self):
        janela = JanelaNovaReserva(self)
        self.wait_window(janela)
        self.carregar_dados()

    def locar(self):
        locacao = self._locacao_selecionada()
        if locacao is None:
            return
        sucesso, msg = self.controller.locar(locacao.id)
        self._mostrar_resultado(sucesso, msg)

    def devolver(self):
        locacao = self._locacao_selecionada()
        if locacao is None:
            return
        sucesso, msg = self.controller.devolver(locacao.id)
        self._mostrar_resultado(sucesso, msg)

    def cancelar(self):
        locacao = self._locacao_selecionada()
        if locacao is None:
            return
        sucesso, msg = self.controller.cancelar(locacao.id)
        self._mostrar_resultado(sucesso, msg)

    def ver_detalhes(self):
        locacao = self._locacao_selecionada()
        if locacao:
            messagebox.showinfo("Detalhes", self.controller.detalhes_locacao(locacao.id), parent=self)

    def _mostrar_resultado(self, sucesso, msg):
        if sucesso:
            self.carregar_dados()
            messagebox.showinfo("Sucesso", msg, parent=self)
        else:
            messagebox.showerror("Erro", msg, parent=self)
