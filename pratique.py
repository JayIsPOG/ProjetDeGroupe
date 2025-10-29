import customtkinter as ctk
import tkinter as tk
import Bag
import dictionnaire

class Pratique(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.bag = Bag.Bag()
        self.player = Bag.Player(self.bag,'Joueur 1')
        self.word_text = ''
        self.color = '#D2B48C'
        self.create_widgets()
  
    def create_widgets(self):
        self.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        self.letter_buttons = {}

        for i in range(7):
            letter = self.player.hand[i].symbol
            
            if i < 4:
                row_num = i
                col_num = 1
            else:
                row_num = i - 4 
                col_num = 2
            button = ctk.CTkButton(
                self, 
                text=letter, 
                fg_color=self.color,
                width=45,
                height=45,
            )
            button.configure(command=lambda t=letter, b=button: self.select_letter(t, b))
            button.grid(row=row_num, column=col_num, pady=(20,20), padx = (20,20))
            self.letter_buttons[button] = False

        self.confirmer = ctk.CTkButton(self,text = "Confirmer le mot",fg_color="red",width = 60,height = 60)
        self.confirmer.grid(row = 1,column = 4,pady=(20,20), padx = (20,20))
        self.word = ctk.CTkLabel(self, text=self.word_text, fg_color="transparent")
        self.word.grid(row=1, column=3, pady=(20,20), padx = (100,100))
    def select_letter(self,letter,button):
        if self.letter_buttons[button] == False:
            self.letter_buttons[button] = True
            self.word_text += letter
            self.word.configure(text = self.word_text)
            button.configure(fg_color = '#343434')
        elif self.letter_buttons[button] == True:
            self.letter_buttons[button] = False
            self.word_text = self.word_text.replace(letter,"",count = 1)
            self.word.configure(text = self.word_text)
            button.configure(fg_color = self.color)
