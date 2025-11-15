import customtkinter as ctk
from dictionnaire import Dictionary

class DictionnairePage(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.textbox = ctk.CTkTextbox(self, height=10)
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.insert("0.0", "Entrez un mot")

        # Liaison propre → chaque saisie appelle read_text
        self.textbox.bind("<KeyRelease>", self.read_text)

        self.result_box = ctk.CTkLabel(self, text="mot invalide")
        self.result_box.grid(row=1, column=0, sticky="nsew")

    def read_text(self, event=None):
        text = self.textbox.get("0.0", "end").strip().upper()

        # Filtrer pour enlever espaces, retours, caractères non A-Z
        word = "".join([c for c in text if c.isalpha()])

        if len(word) == 0:
            self.result_box.configure(text="mot invalide")
            return

        # Dictionnaire.is_word_valid attend un tuple de lettres
        is_valid = Dictionary().is_word_valid(tuple(word))

        self.result_box.configure(text="mot valide" if is_valid else "mot invalide")
