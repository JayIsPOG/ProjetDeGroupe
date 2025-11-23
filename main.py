import customtkinter as ctk
from scrabble import ScrabbleClient
from scrabble import GameWindow
from scrabble import WelcomeWindow  # si tu mets WelcomeWindow dans un fichier séparé
import asyncio
import websockets

if __name__ == "__main__":


    ctk.set_appearance_mode("dark")
    app = WelcomeWindow()
    app.mainloop()