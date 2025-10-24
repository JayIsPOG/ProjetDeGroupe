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

        self.textbox = ctk.CTkTextbox(self, height=20)
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.insert("0.0", "Find A Word")

        self.enterButton = ctk.CTkButton(self, text="Enter", command=self.readText)
        self.enterButton.grid(row=0, column=1, pady=(20,10))
        
        self.tk_textbox = ctk.CTkTextbox(self, activate_scrollbars=False)
        self.tk_textbox.grid(row=0, column=2, sticky="nsew")


        
        
        self.ctk_textbox_scrollbar = ctk.CTkScrollbar(self, command=self.tk_textbox.yview)
        self.ctk_textbox_scrollbar.grid(row=0, column=3, sticky="ns")

        self.tk_textbox.configure(yscrollcommand=self.ctk_textbox_scrollbar.set)

    def readText(self):
        #use find_valid_words
        self.text = self.textbox.get("0.0", "end")
        self.tk_textbox.delete("0.0", "end")
        #self.tk_textbox.insert("0.0", Dictionary.is_word_valid(Dictionary, tuple(self.text[:-1])))
        self.tk_textbox.insert("0.0", Dictionary.find_valid_words(self.text))