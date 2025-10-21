import customtkinter as ctk
import tkinter as tk
class DictionnairePage(ctk.CTkFrame):
    def __init__(self, master=None, series1=None, series2=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.textbox = ctk.CTkTextbox(self)