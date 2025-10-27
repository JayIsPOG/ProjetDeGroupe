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
        xpos = 1 
        ypos = 0
        compteur = -1
        for tiles in self.player.hand:
            print(tiles.symbol)
            compteur += 1
            if compteur ==  4 :
                if xpos < 3 :
                    xpos += 1
                    ypos = 0
            ypos += 1
            self.letters = ( ctk.CTkButton(self, text=tiles.symbol, fg_color=self.color,width=45,height=45,command=lambda t=tiles: self.select_letter(t)))

            self.letters.grid(row=ypos, column=xpos, pady=(20,20), padx = (20,20))

        self.word = ctk.CTkLabel(self, text=self.word_text, fg_color="transparent")
        self.word.grid(row=1, column=3, pady=(20,20), padx = (100,100))

    def select_letter(self,letter):
        if not letter.is_selected:
            self.word_text += letter.symbol
            self.word.configure(text = self.word_text)
            self.letters.configure(fg_color = '#343434')
            letter.is_selected = True
        else :
            letter.is_selected = False
            self.word_text = self.word_text.replace(letter.symbol, '', 1)
            self.word.configure(text = self.word_text)
            self.letters.configure(fg_color = self.color)