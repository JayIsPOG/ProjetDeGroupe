import customtkinter as ctk
import tkinter as tk
from accueil import Accueil
from pratique import Pratique
from dictionnairePage import DictionnairePage
from scrabble import Scrabble
class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x800")
        self.title("Application Principale")
        self.show_accueil()
        self.protocol("WM_DELETE_WINDOW",self.quit)
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
        ##openFile
        print()
    def save_file(self):
        with open("series.txt", "w") as file:
            file.write()
        print()
    def show_scrabble(self, typeOfGame="New"):
        if(typeOfGame == "New"):
            print("New Game")
        else:
            print("Load Game")
            try:
                with open("scrabble.txt", "r") as file:
                    for i in range(15):
                        values = file[i].split()
                print("Fichier 'scrabble.txt' ouvert avec succès.")
                #on reaffiche l'accueil pour actualiser
                self.show_accueil()
            except FileNotFoundError:
                print("Le fichier 'scrabble.txt' n'a pas été trouvé.")
            except Exception as e:
                print(f"Erreur lors de l'ouverture du fichier: {e}")
        self.clear_main_frame()
        self.scrabble = Scrabble(self)
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