import customtkinter as ctk
import tkinter as tk
import Bag
from dictionnaire import Dictionary
from accueil import Accueil

class PressableButton(ctk.CTkButton): 
    def __init__(self, master, text, fg_color, width, height, on_command, off_command):
        super().__init__(master, text = text, fg_color = fg_color, width = width, height = height)
        self.configure(command = self.toggle)
        self.original_color = fg_color
        self.on_command = on_command
        self.off_command = off_command
        self.pressed = False
    def toggle(self):
        self.pressed = not self.pressed
        if self.pressed:
            self.configure(fg_color = '#343434')
            self.on_command()
        else:
            self.configure(fg_color = self.original_color)
            self.off_command()
    def force_off(self):
        self.pressed = False
        self.configure(fg_color = self.original_color)
class Pratique(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.bag = Bag.Bag()
        self.player = Bag.Player(self.bag,'Joueur 1')
        self.word_text = '' ###### mot actuel en train de selectionner
        self.score = 0
        self.word_list = "" ####### tous les mots valides trouves
        self.available_words = Dictionary.find_valid_words([tile.symbol for tile in self.player.hand])
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        self.buttons = []
        for i in range(7):
            letter = self.player.hand[i].symbol
            if i < 4:
                row_num = i
                col_num = 1
            else:
                row_num = i - 4 
                col_num = 2
            button = PressableButton(
                self, 
                text=letter, 
                fg_color='#D2B48C',
                width=45,
                height=45,
                on_command = lambda t=letter: self.select_letter(t),
                off_command = lambda t=letter: self.unselect_letter(t)
            )
            button.grid(row=row_num, column=col_num, pady=(20,20), padx = (20,20))
            self.buttons.append(button)

        self.confirmer = ctk.CTkButton(self,text = "Confirmer le mot",fg_color="red",width = 60,height = 60,command = lambda:self.confirmer_mot())
        self.confirmer.grid(row = 1,column = 4,pady=(20,20), padx = (20,20))

        self.word = ctk.CTkLabel(self, text=self.word_text, fg_color="transparent")
        self.word.grid(row=1, column=3, pady=(20,20), padx = (100,100))

        self.score_box = ctk.CTkLabel(self, text=f'Score : {self.score}/{len(self.available_words) + self.score}', fg_color="green",width = 60,height = 60)
        self.score_box.grid(row=0, column=4, pady=(20,20), padx = (20,20))

        self.terminer = ctk.CTkButton(self,text = "Terminer la pratique",fg_color="blue",width = 60,height = 60,command = lambda:self.terminer_pratique())
        self.terminer.grid(row = 4,column = 4,pady=(20,20), padx = (20,20))
        self.clear_button = ctk.CTkButton(self,text = "Enlever les lettres",fg_color="blue",width = 60,height = 60,command = lambda:self.clear())
        self.clear_button.grid(row = 2,column = 4,pady=(20,20), padx = (20,20))
        self.word_list_box = ctk.CTkLabel(self, text='', fg_color="#C9C6C6",width = 120,height = 60)
        self.word_list_box.grid(row=3, column=3, pady=(20,20), padx = (20,20))
    def clear(self):
        for button in self.buttons:
            button.force_off()
        self.word_text = ''
        self.word.configure(text = self.word_text)
    def select_letter(self,letter):
            self.word_text += letter
            self.word.configure(text = self.word_text)
    def unselect_letter(self,letter):
            i = len(self.word_text) - 1
            while self.word_text[i] != letter: i-=1 #enleve premier caractere a partir de la droite
            self.word_text = self.word_text[:i] + self.word_text[i+1:]
            self.word.configure(text = self.word_text)
    def confirmer_mot(self):
        if self.word_text in self.available_words:
            self.available_words.remove(self.word_text)
            self.word_list += self.word_text + '\n'
            self.score += 1
            self.score_box.configure(text = f'Score : {self.score}/{len(self.available_words) + self.score}')
            self.word_list_box.configure(text = self.word_list)
            self.clear()
    def terminer_pratique(self):
        missing_words = ""
        line_size = 0
        for word in self.available_words:
            missing_words = missing_words + word + ', '
            line_size+= len(word)
            if line_size >= 20: 
                missing_words = missing_words + '\n'
                line_size = 0
        self.recommencer = ctk.CTkButton(self,text = f"Votre score est : {self.score}/{len(self.available_words) + self.score}\nCliquer pour revenir a l'accueil\nMots manquants : {missing_words}",fg_color="#747ACE",width = 400,height = 400,command = lambda:self.recommencer_pratique())
        self.recommencer.place(relx=0.5, rely=0.5, anchor="center") # Exemple: centré
        self.recommencer.lift()

    def recommencer_pratique(self):
        Accueil(self.master)