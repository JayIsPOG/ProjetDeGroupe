import customtkinter as ctk
import tkinter as tk
from dictionnaire import Dictionary
class DictionnairePage(ctk.CTkFrame):
    def __init__(self, master=None, series1=None, series2=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
    def create_widgets(self):
        self.text = ("")

        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.textbox = ctk.CTkTextbox(self, height=10)
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.insert("0.0", "Entrez mot")
        self.textbox.bind('<KeyRelease>', command = self.readText)
        self.textbox.bind('<Key>', command = self.readText)
        
        self.result_box = ctk.CTkLabel(self, text = 'mot invalide')
        self.result_box.grid(row=1, column=0, sticky="nsew")

    def readText(self, event):
        self.text = self.textbox.get("0.0", "end")
        self.result_box.configure(text = 'mot valide' if Dictionary.is_word_valid(Dictionary, tuple(self.text[:-1].upper())) else 'mot invalide')
