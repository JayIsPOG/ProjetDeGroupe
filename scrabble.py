import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from testCopy import JeuScrabble

class Accueil(ctk.CTkFrame):
    def __init__(self, master=None, series1=None, series2=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
    def create_widgets(self):
        
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=0, pady=(10,10))