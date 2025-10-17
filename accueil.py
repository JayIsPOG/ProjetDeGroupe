import customtkinter as ctk
import tkinter as tk
class Accueil(ctk.CTkFrame):
    def __init__(self, master=None, series1=None, series2=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.ScrabbleLabel = ctk.CTkLabel(self, text="Scrabble", fg_color="transparent")
        self.ScrabbleLabel.grid(row=0, column=1, pady=(10,10))
        self.newGameButton = ctk.CTkButton(self, text="Nouvelle Partie", command=self.master.show_scrabble)
        self.newGameButton.grid(row=1, column=0, pady=(20,10))
        self.loadGameButton = ctk.CTkButton(self, text="Charger un partie", command=self.master.show_scrabble)
        self.loadGameButton.grid(row=1, column=2, pady=(20,10))

        self.PracticeLabel = ctk.CTkLabel(self, text="Pratique", fg_color="transparent")
        self.PracticeLabel.grid(row=3, column=1, pady=(10,10))
        self.newGameButton = ctk.CTkButton(self, text="Nouvelle Partie", command=self.master.show_scrabble)
        self.newGameButton.grid(row=4, column=0, pady=(20,10))

        self.DictionnairyLabel = ctk.CTkLabel(self, text="Dictionnaire", fg_color="transparent")
        self.DictionnairyLabel.grid(row=6, column=1, pady=(10,10))
        self.newGameButton = ctk.CTkButton(self, text="Nouvelle Partie", command=self.master.show_scrabble)
        self.newGameButton.grid(row=7, column=0, pady=(20,10))


