# view/create_vehicle_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from model.veiculo import Categoria
from model.ExcecoesPersonalizadas import PlacaInvalidaError

class CreateVehicleView:
    def __init__(self, root, repo, refresh_callback):
        self.repo = repo
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(root)
        self.window.title("Novo Veículo")

        # Tipo
        tk.Label(self.window, text="Tipo").pack()
        self.tipo = ttk.Combobox(self.window, values=["carro", "motorhome"])
        self.tipo.pack()

        # Placa
        tk.Label(self.window, text="Placa").pack()
        self.placa = tk.Entry(self.window)
        self.placa.pack()

        # Categoria
        tk.Label(self.window, text="Categoria").pack()
        self.categoria = ttk.Combobox(
            self.window,
            values=[c.name for c in Categoria]
        )
        self.categoria.pack()

        # Taxa
        tk.Label(self.window, text="Taxa diária").pack()
        self.taxa = tk.Entry(self.window)
        self.taxa.pack()

        tk.Button(self.window, text="Salvar", command=self.save).pack(pady=10)

    def save(self):
        try:
            tipo = self.tipo.get()
            placa = self.placa.get()
            categoria = Categoria[self.categoria.get()]
            taxa = float(self.taxa.get())

            self.repo.adicionar(tipo, placa, categoria, taxa)

            self.refresh_callback()
            self.window.destroy()

        except PlacaInvalidaError as e:
            messagebox.showerror("Erro", str(e))

        except ValueError as e:
            messagebox.showerror("Erro", str(e))

        except Exception as e:
            messagebox.showerror("Erro inesperado", str(e))