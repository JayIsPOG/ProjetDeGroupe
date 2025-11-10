import customtkinter as ctk
import tkinter as tk
from dictionnaire import Dictionary
from accueil import Accueil
from dictionnaire import Dictionary

class Wordle(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.inputText = ""
        self.ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.lettresIncorrectes = ""
        self.lettresMalPlacees = ""
        self.lettresCorrectes = ""
        self.mot = Dictionary.random_word(Dictionary, "dictionnaireWordlePossible.txt")
        self.essaies = []

        self.create_widgets()
        
        
    def create_widgets(self):
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        #Grille Des Essaies
        self.GrilleEssaies = set()
        for i in range(5):
            for j in range(6):
                if len(self.essaies) > j:
                    color = "grey"
                    if(self.essaies[j][i] == self.mot[i]):
                        color = "green"
                    elif(self.essaies[j][i] in self.mot):
                        color = "orange"
                    else:
                        color = "red"

                    label = ctk.CTkLabel(self.master, text=self.essaies[j][i], fg_color=color, width=50, height=50, text_color="white", font=("arial", 25))
                    label.place(x=i*60+20,y=j*60+20)
                    self.GrilleEssaies.add(label)
                else:
                    label = ctk.CTkLabel(self.master, text="", fg_color="grey", width=50, height=50, text_color="white", font=("arial", 25))
                    label.place(x=i*60+20,y=j*60+20)
                    self.GrilleEssaies.add(label)
        
        #Grille Des Lettres
        self.GrilleLettres = set()
        for i in range(3):
            for j in range(7):
                self.creerBouttonLettre(i*7+j, j*60+360, i*60+20)
        for j in range(5):
            self.creerBouttonLettre(i*7+j+7, j*60+420, i*60+80)
        
        #Input Mot
        self.input = ctk.CTkTextbox(self.master, fg_color="grey", width=300, height=50, text_color="white", font=("arial", 25))
        self.input.insert("0.0", self.inputText)
        self.input.place(x=350,y=300)

        #Entrer
        self.EnterButton = ctk.CTkButton(self.master, text="Entrer", width=100, height=50, command=self.lireInput, fg_color="blue")
        self.EnterButton.place(x=675,y=300)
        
    def creerBouttonLettre(self, index, posx, posy):
        lettre = self.ALPHABET[index]
        color = "grey"
        if(lettre in self.lettresIncorrectes):
            color = "red"
        if(lettre in self.lettresCorrectes):
            color = "green"
        elif(lettre in self.lettresMalPlacees):
            color = "orange"
        boutton = ctk.CTkButton(self.master, text=lettre, width=40, height=40, command=lambda: self.bouttonLettre(lettre), fg_color=color)
        boutton.place(y=posy,x=posx)
        self.GrilleLettres.add(boutton)

    def bouttonLettre(self, lettre):
        #self.inputText += lettre
        mot = self.input.get("0.0", "5.0").upper().rstrip()
        mot += lettre
        self.inputText = mot
        self.input.delete("0.0", "end")
        self.input.insert("0.0", mot)

    def lireInput(self):
        mot = self.input.get("0.0", "5.0").upper().rstrip()
        self.input.delete("0.0", "end")
        if len(mot) == 5:
            if Dictionary.is_word_valid(Dictionary, tuple(mot), "dictionnaireWordleAllowed.txt"):
                self.essaies.append(mot)
                if self.verifieMot(mot):
                    print("Yes")
                #else:
                    #print(self.mot)
            self.create_widgets()
        if(len(self.essaies) == 6):
            print(self.mot)

    def verifieMot(self, mot):
        for i in range(len(mot)):
            if mot[i] == self.mot[i]:
                self.lettresCorrectes += mot[i]
            elif mot[i] in self.mot:
                self.lettresMalPlacees += mot[i]
            else:
                self.lettresIncorrectes += mot[i]
        return mot.upper().rstrip() == self.mot.upper().rstrip()

    