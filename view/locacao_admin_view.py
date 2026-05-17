import tkinter as tk
from tkinter import messagebox, ttk

from control.locacao_controller import LocacaoController
from model.locacao import StatusLocacao


class JanelaCadastroLocacao(tk.Toplevel):
    def __init__(self, master=None, locacao_existente=None):
        super().__init__(master)
        self.controller = LocacaoController()
        self.locacao_existente = locacao_existente

        self.title("Editar Locacao" if locacao_existente else "Nova Locacao")
        self.geometry("420x360")

        tk.Label(self, text=self.title(), font=("Helvetica", 16, "bold")).pack(pady=10)

        self.cb_veiculo = self._criar_combo("Veiculo")
        self.txt_inicio = self._criar_entrada("Data inicio (YYYY-MM-DD)")
        self.txt_fim = self._criar_entrada("Data fim (YYYY-MM-DD)")
        self.cb_status = self._criar_combo("Status", [s.value for s in StatusLocacao])
        self.cb_estrategia = self._criar_combo("Estrategia", ["PADRAO", "VIP"])

        tk.Button(self, text="Salvar", command=self.salvar).pack(pady=18)
        self.carregar_veiculos()
        self.preencher_edicao()

    def _criar_entrada(self, texto):
        frame = tk.Frame(self)
        frame.pack(fill="x", padx=24, pady=4)
        tk.Label(frame, text=texto).pack(side="left")
        entrada = tk.Entry(frame)
        entrada.pack(side="right", expand=True, fill="x")
        return entrada

    def _criar_combo(self, texto, valores=None):
        frame = tk.Frame(self)
        frame.pack(fill="x", padx=24, pady=4)
        tk.Label(frame, text=texto).pack(side="left")
        combo = ttk.Combobox(frame, values=valores or [], state="readonly")
        combo.pack(side="right", expand=True, fill="x")
        return combo

    def carregar_veiculos(self):
        valores = [v.placa for v in self.controller.veiculo_controller.listar_veiculos()]
        self.cb_veiculo["values"] = valores
        if valores:
            self.cb_veiculo.current(0)
        self.cb_status.current(0)
        self.cb_estrategia.current(0)

    def preencher_edicao(self):
        if self.locacao_existente is None:
            return

        self.cb_veiculo.set(self.locacao_existente.veiculo.placa)
        self.txt_inicio.insert(0, self.locacao_existente.data_inicio.strftime("%Y-%m-%d"))
        self.txt_fim.insert(0, self.locacao_existente.data_fim.strftime("%Y-%m-%d"))
        self.cb_status.set(self.locacao_existente.status.value)
        self.cb_estrategia.set(self.controller.nome_estrategia(self.locacao_existente))

    def salvar(self):
        placa = self.cb_veiculo.get()
        inicio = self.txt_inicio.get()
        fim = self.txt_fim.get()
        status = self.cb_status.get()
        estrategia = self.cb_estrategia.get()

        if self.locacao_existente is None:
            sucesso, msg = self.controller.criar_locacao(
                placa, inicio, fim, status, estrategia, validar_disponibilidade=False
            )
        else:
            sucesso, msg = self.controller.atualizar_locacao(
                self.locacao_existente.id, placa, inicio, fim, status, estrategia
            )

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)


class JanelaListagemLocacoes(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = LocacaoController()
        self.title("Locacoes - Admin")
        self.geometry("900x430")
        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        tk.Label(self, text="Locacoes - Administrador", font=("Helvetica", 16, "bold")).pack(pady=10)

        colunas = ("ID", "Placa", "Tipo", "Inicio", "Fim", "Status", "Estrategia")
        self.tree = ttk.Treeview(self, columns=colunas, show="headings")
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=110)
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        frame = tk.Frame(self)
        frame.pack(fill="x", padx=20, pady=5)
        tk.Button(frame, text="Novo", width=12, command=self.abrir_novo).pack(side="left", padx=5)
        tk.Button(frame, text="Editar", width=12, command=self.abrir_editar).pack(side="left", padx=5)
        tk.Button(frame, text="Ver Detalhes", width=14, command=self.ver_detalhes).pack(side="left", padx=5)
        tk.Button(frame, text="Remover", width=12, command=self.remover).pack(side="left", padx=5)
        tk.Button(frame, text="Fechar", width=12, command=self.destroy).pack(side="right", padx=5)

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
                self.controller.nome_estrategia(locacao),
            ))

    def _locacao_selecionada(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma locacao.", parent=self)
            return None
        id_locacao = self.tree.item(selecionado[0])["values"][0]
        return self.controller.buscar_por_id(id_locacao)

    def abrir_novo(self):
        janela = JanelaCadastroLocacao(self)
        self.wait_window(janela)
        self.carregar_dados()

    def abrir_editar(self):
        locacao = self._locacao_selecionada()
        if locacao is None:
            return
        janela = JanelaCadastroLocacao(self, locacao)
        self.wait_window(janela)
        self.carregar_dados()

    def ver_detalhes(self):
        locacao = self._locacao_selecionada()
        if locacao:
            messagebox.showinfo("Detalhes", self.controller.detalhes_locacao(locacao.id), parent=self)

    def remover(self):
        locacao = self._locacao_selecionada()
        if locacao is None:
            return
        if not messagebox.askyesno("Confirmar", "Remover esta locacao?", parent=self):
            return
        sucesso, msg = self.controller.remover_locacao(locacao.id)
        if sucesso:
            self.carregar_dados()
            messagebox.showinfo("Sucesso", msg, parent=self)
        else:
            messagebox.showerror("Erro", msg, parent=self)
