# view/main_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from views.criar_veiculo_view import CreateVehicleView

class MainView:
    def __init__(self, root, repo):
        self.root = root
        self.repo = repo

        self.root.title("Locadora de Veículos")

        # Tabela
        self.tree = ttk.Treeview(
            root,
            columns=("Placa", "Tipo", "Categoria", "Taxa"),
            show="headings"
        )

        for col in ("Placa", "Tipo", "Categoria", "Taxa"):
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)

        # Botões
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Button(frame, text="Novo", command=self.open_create).pack(side="left", padx=5)
        tk.Button(frame, text="Ver", command=self.view_vehicle).pack(side="left", padx=5)
        tk.Button(frame, text="Remover", command=self.delete_vehicle).pack(side="left", padx=5)

        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for v in self.repo.listar():
            tipo = v.__class__.__name__
            self.tree.insert("", "end", values=(
                v.placa,
                tipo,
                v.categoria.name,
                v.taxa_diaria
            ))

    def get_selected(self):
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0])["values"]

    def open_create(self):
        CreateVehicleView(self.root, self.repo, self.refresh_table)

    def view_vehicle(self):
        v = self.get_selected()
        if v:
            messagebox.showinfo(
                "Detalhes",
                f"Placa: {v[0]}\nTipo: {v[1]}\nCategoria: {v[2]}\nTaxa: {v[3]}"
            )

    def delete_vehicle(self):
        v = self.get_selected()
        if v:
            self.repo.remover(v[0])
            self.refresh_table()