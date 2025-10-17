import customtkinter as ctk
import tkinter as tk
class Accueil(ctk.CTkFrame):
    def __init__(self, master=None, series1=None, series2=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.button = ctk.CTkButton(self, text="Nouvelle Partie", command=self.master.show_scrabble)
        self.button.grid(row=0, column=0, pady=(20,10))
        self.label = ctk.CTkLabel(self, text="Scrabble", fg_color="transparent")
        self.label.grid(row=1, column=0, pady=(10,10))
