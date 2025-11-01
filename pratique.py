import customtkinter as ctk
import tkinter as tk
import Bag
from dictionnaire import Dictionary
from accueil import Accueil
class Pratique(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.bag = Bag.Bag()
        self.player = Bag.Player(self.bag,'Joueur 1')
        self.word_text = ''
        self.color = '#D2B48C'
        self.score = 0
        self.word_list = []
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

        self.confirmer = ctk.CTkButton(self,text = "Confirmer le mot",fg_color="red",width = 60,height = 60,command = lambda:self.confirmer_mot())
        self.confirmer.grid(row = 1,column = 4,pady=(20,20), padx = (20,20))

        self.word = ctk.CTkLabel(self, text=self.word_text, fg_color="transparent")
        self.word.grid(row=1, column=3, pady=(20,20), padx = (100,100))

        self.score_box = ctk.CTkLabel(self, text=f'Score : {self.score}', fg_color="green",width = 60,height = 60)
        self.score_box.grid(row=0, column=4, pady=(20,20), padx = (20,20))

        self.terminer = ctk.CTkButton(self,text = "Terminer la pratique",fg_color="blue",width = 60,height = 60,command = lambda:self.terminer_pratique())
        self.terminer.grid(row = 4,column = 4,pady=(20,20), padx = (20,20))
        word_list_box = ctk.CTkLabel(self, text='', fg_color="#C9C6C6",width = 120,height = 60)
        word_list_box.grid(row=3, column=3, pady=(20,20), padx = (20,20))

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
    def confirmer_mot(self):
        if Dictionary.is_word_valid(Dictionary,tuple(self.word_text)) and not self.word_text in self.word_list:
            self.word_list.append(self.word_text)
            self.score += len(self.word_text)
            self.score_box.configure(text = f'Score : {self.score}')
            text1=''
            for word in self.word_list:
                text1 += (word + '\n')
            word_list_box = ctk.CTkLabel(self, text=text1, fg_color="#C9C6C6",width = 60,height = 60)
            word_list_box.grid(row=3, column=3, pady=(20,20), padx = (20,20))
    def terminer_pratique(self):
        self.recommencer = ctk.CTkButton(self,text = f"Votre score est : {self.score}\nCliquer pour revenir a l'accueil",fg_color="#747ACE",width = 400,height = 400,command = lambda:self.recommencer_pratique())
        self.recommencer.place(relx=0.5, rely=0.5, anchor="center") # Exemple: centré
        self.recommencer.lift()

    def recommencer_pratique(self):
        Accueil(self.master)