import customtkinter as ctk
import tkinter as tk
from PIL import Image
class Accueil(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
    def create_widgets(self):
        self.scrabbleIcon = ctk.CTkImage(light_image=Image.open("sprites//scrabble.png"), size=(40, 40))
        self.pratiqueIcon = ctk.CTkImage(light_image=Image.open("sprites//practice.png"), size=(40, 40))
        self.wordleIcon = ctk.CTkImage(light_image=Image.open("sprites//wordle.png"), size=(40, 40))
        self.dictionnaireIcon = ctk.CTkImage(light_image=Image.open("sprites//dictionnary.png"), size=(40, 40))

        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.ScrabbleLabel = ctk.CTkLabel(self, text="Scrabble", fg_color="transparent")
        self.ScrabbleLabel.grid(row=1, column=1, pady=(10,10))
        self.scrabbleImage = ctk.CTkLabel(self, text="", fg_color="transparent",image=self.scrabbleIcon)
        self.scrabbleImage.grid(row=1, column=0, pady=(10,10), padx=(10,10))
        self.newGameButton = ctk.CTkButton(self, text="Nouvelle Partie", command=self.master.show_scrabble)
        self.newGameButton.grid(row=1, column=2, pady=(20,10), padx=(20,20))
        self.loadGameButton = ctk.CTkButton(self, text="Charger un partie", command=self.master.open_file)
        self.loadGameButton.grid(row=1, column=3, pady=(20,10), padx=(20,20))

        self.PracticeLabel = ctk.CTkLabel(self, text="Pratique", fg_color="transparent")
        self.PracticeLabel.grid(row=2, column=1, pady=(10,10))
        self.pratiqueImage = ctk.CTkLabel(self, text="", fg_color="transparent",image=self.pratiqueIcon)
        self.pratiqueImage.grid(row=2, column=0, pady=(10,10), padx=(10,10))
        self.newPracticeButton = ctk.CTkButton(self, text="Nouvelle Partie", command=self.master.show_pratique)
        self.newPracticeButton.grid(row=2, column=2, pady=(20,10))

        self.WordleLabel = ctk.CTkLabel(self, text="Wordle", fg_color="transparent")
        self.WordleLabel.grid(row=3, column=1, pady=(10,10))
        self.wordleImage = ctk.CTkLabel(self, text="", fg_color="transparent",image=self.wordleIcon)
        self.wordleImage.grid(row=3, column=0, pady=(10,10), padx=(10,10))
        self.newWordleButton = ctk.CTkButton(self, text="Nouvelle Partie", command=self.master.show_wordle)
        self.newWordleButton.grid(row=3, column=2, pady=(20,10))

        self.DictionnairyLabel = ctk.CTkLabel(self, text="Dictionnaire", fg_color="transparent")
        self.DictionnairyLabel.grid(row=4, column=1, pady=(10,10))
        self.dictionnaireImage = ctk.CTkLabel(self, text="", fg_color="transparent",image=self.dictionnaireIcon)
        self.dictionnaireImage.grid(row=4, column=0, pady=(10,10), padx=(10,10))
        self.dictionnairyButton = ctk.CTkButton(self, text="Ouvrir", command=self.master.show_dictionnaire)
        self.dictionnairyButton.grid(row=4, column=2, pady=(20,10))


