import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from control.veiculo_controller import VeiculoController


class JanelaCadastroVeiculo(tk.Toplevel):
    def __init__(self, master=None, veiculo_existente=None):
        super().__init__(master)

        self.veiculo_existente = veiculo_existente
        self.controller = VeiculoController()

        self.title("Atualizar Veiculo" if veiculo_existente else "Cadastro de Novo Veiculo")
        self.geometry("400x350")

        texto_titulo = "Atualizar Veiculo" if veiculo_existente else "Cadastrar Veiculo"
        lbl_titulo = tk.Label(self, text=texto_titulo, font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        frame_placa = tk.Frame(self)
        frame_placa.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_placa, text="Placa:").pack(side="left")
        self.txt_placa = tk.Entry(frame_placa)
        self.txt_placa.pack(side="right")

        frame_tipo = tk.Frame(self)
        frame_tipo.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_tipo, text="Tipo:").pack(side="left")
        self.cb_tipo = ttk.Combobox(frame_tipo, values=["carro", "motorhome"], state="readonly")
        self.cb_tipo.current(0)
        self.cb_tipo.pack(side="right", expand=True, fill="x")

        frame_cat = tk.Frame(self)
        frame_cat.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_cat, text="Categoria:").pack(side="left")
        self.cb_categoria = ttk.Combobox(frame_cat, values=["ECONOMICO", "EXECUTIVO"], state="readonly")
        self.cb_categoria.current(0)
        self.cb_categoria.pack(side="right", expand=True, fill="x")

        frame_taxa = tk.Frame(self)
        frame_taxa.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_taxa, text="Taxa Diaria (R$):").pack(side="left")
        self.txt_taxa = tk.Entry(frame_taxa)
        self.txt_taxa.pack(side="right", expand=True, fill="x")

        texto_botao = "Atualizar Veiculo" if veiculo_existente else "Salvar Veiculo"
        btn_cadastrar = tk.Button(self, text=texto_botao, command=self.solicitar_cadastro)
        btn_cadastrar.pack(pady=20)

        if self.veiculo_existente:
            self.preencher_campos_edicao()

    def preencher_campos_edicao(self):
        self.txt_placa.insert(0, self.veiculo_existente.placa)
        self.txt_placa.config(state="disabled")
        self.cb_tipo.set(self.veiculo_existente.__class__.__name__.lower())
        self.cb_categoria.set(self.veiculo_existente.categoria.name)
        self.txt_taxa.insert(0, f"{self.veiculo_existente.taxa_diaria:.2f}".replace(".", ","))

    def solicitar_cadastro(self):
        placa = self.txt_placa.get().strip().upper()
        tipo = self.cb_tipo.get().strip()
        categoria = self.cb_categoria.get().strip()
        taxa_str = self.txt_taxa.get().strip()

        if self.veiculo_existente:
            sucesso, msg = self.controller.atualizar_veiculo(placa, tipo, categoria, taxa_str)
        else:
            sucesso, msg = self.controller.salvar_veiculo(placa, tipo, categoria, taxa_str)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)
