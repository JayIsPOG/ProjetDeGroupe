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
        menu_bar.add_cascade(label="Scrabble", menu=view_menu)
        view_menu.add_command(label="Nouvelle partie", command=self.show_scrabble("New"))
        view_menu.add_command(label="Charger une partie", command=self.show_scrabble("Load"))
    def open_file(self):
        ##openFile
        print()
    def save_file(self):
        ##sauvegarde
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
                        if len(values) == 2:
                            self.series1.append(float(values[0]))
                            self.series2.append(float(values[1]))
                print("Fichier 'scrabble.txt' ouvert avec succès.")
                #on reaffiche l'accueil pour actualiser
                self.show_accueil()
            except FileNotFoundError:
                print("Le fichier 'series.txt' n'a pas été trouvé.")
            except Exception as e:
                print(f"Erreur lors de l'ouverture du fichier: {e}")
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