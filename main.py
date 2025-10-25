import customtkinter as ctk
import tkinter as tk
from accueil import Accueil
from pratique import Pratique
from dictionnairePage import DictionnairePage
from scrabble import Scrabble
class MainApp(ctk.CTk):
    def __init__(self):
        self.scrabble = None
        super().__init__()
        self.geometry("700x700")
        self.title("Application Principale")
        self.show_accueil()
        self.protocol("WM_DELETE_WINDOW", self.quit)
    def show_accueil(self):
        self.clear_main_frame()
        self.accueil = Accueil(master=self)
        self.create_menu()
        
    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Ouvrir", command=self.open_file)
        file_menu.add_command(label="Enregistrer", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.quit)
        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Affichage", menu=view_menu)
        view_menu.add_command(label="Accueil", command=self.show_accueil)
        view_menu.add_command(label="Partique", command=self.show_pratique)
        view_menu.add_command(label="Dictionnaire", command=self.show_dictionnaire)
    def open_file(self):
        self.clear_main_frame()
        self.scrabble = Scrabble(self, 'game.txt')
        self.scrabble.pack(expand=True, fill="both")
        self.create_menu()
    def save_file(self):
        if self.scrabble:
            self.scrabble.save_game('game.txt')
    def show_scrabble(self, typeOfGame="New"):
        self.clear_main_frame()
        if(typeOfGame == "New"):
            self.scrabble = Scrabble(self)
        else:
            self.scrabble = Scrabble(self, 'game.txt')
        self.scrabble.pack(expand=True, fill="both")
        self.create_menu()
    def show_pratique(self):
        self.clear_main_frame()
        self.pratique = Pratique(self)
        self.create_menu()
    def show_dictionnaire(self):
        self.clear_main_frame()
        self.dictionnaire = DictionnairePage(self)
        self.create_menu()
    def clear_main_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()