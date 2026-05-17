import os
import sys
import tkinter as tk

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from view.locacao_admin_view import JanelaListagemLocacoes
from view.locacao_usuario_view import JanelaLocacaoUsuario
from view.veiculo_list_view import JanelaListagemVeiculos


class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Locadora de Veiculos")
        self.geometry("520x260")
        self.criar_menu()
        self.criar_conteudo()

    def criar_menu(self):
        barra_menu = tk.Menu(self)

        menu_cadastro = tk.Menu(barra_menu, tearoff=0)
        menu_cadastro.add_command(label="Veiculo", command=self.abrir_veiculos)
        menu_cadastro.add_command(label="Locacoes (Admin)", command=self.abrir_locacoes_admin)
        barra_menu.add_cascade(label="Cadastro", menu=menu_cadastro)

        menu_acao = tk.Menu(barra_menu, tearoff=0)
        menu_acao.add_command(label="Locar Veiculo", command=self.abrir_locacao_usuario)
        barra_menu.add_cascade(label="Acao", menu=menu_acao)

        self.config(menu=barra_menu)

    def criar_conteudo(self):
        tk.Label(self, text="Locadora de Veiculos", font=("Helvetica", 18, "bold")).pack(pady=(48, 12))
        tk.Label(self, text="Use o menu superior para acessar cadastros e acoes.").pack()

    def abrir_veiculos(self):
        JanelaListagemVeiculos(self)

    def abrir_locacoes_admin(self):
        JanelaListagemLocacoes(self)

    def abrir_locacao_usuario(self):
        JanelaLocacaoUsuario(self)


if __name__ == "__main__":
    JanelaPrincipal().mainloop()
