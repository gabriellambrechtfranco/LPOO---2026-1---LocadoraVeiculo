import tkinter as tk
from model.veiculo_repository import VeiculoRepository
from views.veiculo_list_view import MainView

root = tk.Tk()

repo = VeiculoRepository()
app = MainView(root, repo)

root.mainloop()