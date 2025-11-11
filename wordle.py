import customtkinter as ctk
import tkinter as tk
from dictionnaire import Dictionary
from accueil import Accueil
from dictionnaire import Dictionary

class Wordle(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.dictionnaire = "dictionnaireWordleAllowed.txt"
        self.dictionnairePossible = "dictionnaireWordlePossible.txt"

        self.inputText = ""
        self.lettresIncorrectes = ""
        self.lettresMalPlacees = ""
        self.lettresCorrectes = ""
        self.mot = Dictionary.random_word(Dictionary, self.dictionnairePossible)
        self.essaies = []
        self.GrilleEssaies = set()
        self.GrilleLettres = set()
        self.create_widgets()

        self.master.bind('<Return>', self.lireInput)
        self.master.bind('<Key>', self.clavierLettre)
        self.master.bind('<BackSpace>', self.motBackspace)
        
    def create_widgets(self):
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.creerGrilleEssaies()

        self.creerGrilleBouttonLettre()

        #Entrer
        self.EnterButton = ctk.CTkButton(self.master, text="Entrer", width=400, height=50, command=lambda: self.lireInput(""), fg_color="blue")
        self.EnterButton.place(x=360,y=300)

        #Vider
        self.EnterButton = ctk.CTkButton(self.master, text="Vider", width=100, height=40, command=self.viderMot, fg_color="red")
        self.EnterButton.place(x=660,y=200)

        #Sélection de dictionnaire
        self.BouttonDictionnaires = ctk.CTkSegmentedButton(self.master, values=["Anglais", "Français", "Scrabble (Français)"],command=self.selectionnerDictionnaire)
        self.BouttonDictionnaires.set("Anglais")
        self.BouttonDictionnaires.place(x=400,y=500)

    def creerGrilleEssaies(self):
        for essaie in self.GrilleEssaies:
            essaie.destroy()
        
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

                    label = ctk.CTkLabel(self.master, text=self.essaies[j][i], fg_color=color, width=50, height=50, text_color="white", font=("calibri", 25))
                    label.place(x=i*60+20,y=j*60+20)
                    self.GrilleEssaies.add(label)
                elif(len(self.essaies) >= j and len(self.inputText) > i):
                    label = ctk.CTkLabel(self.master, text=self.inputText[i], fg_color="grey", width=50, height=50, text_color="white", font=("calibri", 25))
                    label.place(x=i*60+20,y=j*60+20)
                    self.GrilleEssaies.add(label)
                else:
                    label = ctk.CTkLabel(self.master, text="", fg_color="grey", width=50, height=50, text_color="white", font=("calibri", 25))
                    label.place(x=i*60+20,y=j*60+20)
                    self.GrilleEssaies.add(label)

    def creerGrilleBouttonLettre(self):
        for essaie in self.GrilleLettres:
            essaie.destroy()
        for i in range(3):
            for j in range(7):
                self.creerBouttonLettre(i*7+j, j*60+360, i*60+20)
        for j in range(5):
            self.creerBouttonLettre(i*7+j+7, j*60+360, i*60+80)
            
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
        if len(self.inputText) < 5:
            self.inputText += lettre
            self.inputText = self.inputText
            self.creerGrilleEssaies()

    def clavierLettre(self, event):
        if event.char and len(self.inputText) < 5:
            self.inputText += event.char.upper()
            self.inputText = self.inputText
            self.creerGrilleEssaies()

    def lireInput(self, event):
        if len(self.inputText) == 5:
            if Dictionary.is_word_valid(Dictionary, tuple(self.inputText), self.dictionnaire):
                self.essaies.append(self.inputText)
                if self.verifieMot(self.inputText):
                    print("Mot Trouvé")
                    self.label = ctk.CTkLabel(self.master, text="PARTIE TERMINÉE: VOUS AVEZ TROUVÉ LE MOT", fg_color="transparent", width=100, height=50, text_color="black", font=("calibri", 25))
                    self.label.place(x=0,y=400)
                    #besoin de delete les labels
                elif len(self.essaies) == 6:
                    self.label = ctk.CTkLabel(self.master, text="PARTIE TERMINÉE: VOUS N'AVEZ PAS TROUVÉ: " + self.mot, fg_color="transparent", width=100, height=50, text_color="black", font=("calibri", 25))
                    self.label.place(x=0,y=400)
            else:
                self.label = ctk.CTkLabel(self.master, text="Mot Invalide", fg_color="transparent", width=100, height=50, text_color="black", font=("calibri", 25))
                self.label.place(x=100,y=400)
            self.creerGrilleBouttonLettre()
            self.creerGrilleEssaies()

    def viderMot(self):
        self.inputText = ""
        self.creerGrilleEssaies()

    def motBackspace(self, event):
        self.inputText = self.inputText[:-1]
        self.creerGrilleEssaies()

    def verifieMot(self, mot):
        for i in range(len(mot)):
            if mot[i] == self.mot[i]:
                self.lettresCorrectes += mot[i]
            elif mot[i] in self.mot:
                self.lettresMalPlacees += mot[i]
            else:
                self.lettresIncorrectes += mot[i]
        return mot.upper().rstrip() == self.mot.upper().rstrip()

    def selectionnerDictionnaire(self, dictionnaire):
        if dictionnaire == "Anglais":
            self.dictionnaire = "dictionnaireWordleAllowed.txt"
            self.dictionnairePossible = "dictionnaireWordlePossible.txt"
        elif dictionnaire == "Français":
            self.dictionnaire = "dictionnaireFrancais.txt"
            self.dictionnairePossible = "dictionnaireFrancais.txt"
        elif dictionnaire == "Scrabble (Français)":
            self.dictionnaire = "dictionnaireScrabbleFrancais.txt"
            self.dictionnairePossible = "dictionnaireScrabbleFrancais.txt"
        self.recommencerPartie()
    
    def recommencerPartie(self):
        self.inputText = ""
        self.lettresIncorrectes = ""
        self.lettresMalPlacees = ""
        self.lettresCorrectes = ""
        self.mot = Dictionary.random_word(Dictionary, self.dictionnairePossible)
        self.essaies = []
        self.creerGrilleBouttonLettre()
        self.creerGrilleEssaies()
        