import customtkinter as ctk
import tkinter as tk
from accueil import Accueil
from pratique import Pratique
from dictionnaire import Dictionnaire
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x600")
        self.title("Application Principale")
        self.show_accueil()
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
        view_menu.add_command(label="Scrabble", command=self.show_scrabble)
        view_menu.add_command(label="Pratique", command=self.show_pratique)
        view_menu.add_command(label="Dictionnaire", command=self.show_dictionnaire)
    def open_file(self):
        ##openFile
        print()
    def save_file(self):
        ##sauvegarde
        print()
    def show_scrabble(self):
        print()
    def show_pratique(self):
        self.clear_main_frame()
        self.formulaire = Pratique(self)
        self.create_menu()
    def show_dictionnaire(self):
        self.clear_main_frame()
        self.formulaire = Dictionnaire(self)
        self.create_menu()
    def clear_main_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()