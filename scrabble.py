import matplotlib.pyplot as plt
import numpy as np
from Bag import Tile
from Bag import Player
from Bag import Bag
from dictionnaire import Dictionary
import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ajouter une fonction pour flush la main pis repiger au cas ou aucun mot son possibles
# save and load files et sauvegarder les scores
# regarder si sac est vide pour finir la partie
# afficher qui est le joueur actuel

word_score = np.array([
     [3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 3],
     [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
     [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
     [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
     [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 3],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
     [1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
     [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
     [1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
     [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
     [3, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 3]
     ])
letter_multiplier = np.array([
     [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1], 
     [1, 1, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 1, 1], 
     [1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1], 
     [2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2], 
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
     [1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1], 
     [1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1], 
     [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1], 
     [1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1], 
     [1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 3, 1], 
     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
     [2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2], 
     [1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1], 
     [1, 1, 1, 1, 1, 3, 1, 1, 1, 3, 1, 1, 1, 1, 1], 
     [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
     ])
class Scrabble(ctk.CTkFrame):
     def __init__(self, master=None, file_name = None):
          super().__init__(master)
          self.master = master
          self.bag = Bag()
          self.players = (Player(self.bag, ""), Player(self.bag, ""))
          self.current_player = False
          self.tile_board = np.full((15, 15), None)
          self.is_new = np.zeros((15, 15))
          self.selected_tile = None
          if file_name:
               self.bag.tiles = []
               self.players[0].hand = []
               self.players[1].hand = []
               self.tile_board = np.full((15, 15), None)
               self.is_new = np.zeros((15, 15))
               self.selected_tile = None
               with open(file_name, 'r') as file: ## ajouter message erreur si file existe pas
                    lines = [line for line in file]
                    self.current_player = bool(lines[0].strip())
                    self.players[0].score = int(lines[1].strip())
                    self.players[1].score = int(lines[2].strip())
                    self.is_first_turn = bool(lines[3].strip())
                    index = 4
                    while lines[index] != '\n':
                         l = lines[index].strip()
                         self.players[0].hand.append(Tile(l[0], int(l[1:])))
                         index += 1
                    self.players[0].hand_max_size = len(self.players[0].hand)
                    index += 1
                    while lines[index] != '\n':
                         l = lines[index].strip()
                         self.players[1].hand.append(Tile(l[0], int(l[1:])))
                         index += 1
                    self.players[1].hand_max_size = len(self.players[1].hand)
                    index += 1
                    for i in range(0, 15):
                         for j in range(0, 15):
                              if lines[index] != '\n':
                                   l = lines[index].strip()
                                   self.tile_board[i, j] = Tile(l[0], int(l[1:]))
                                   self.letter.set_position((j + 0.5, i + 0.5))
                                   self.letter.set_text(self.tile_board[i, j].symbol)
                                   self.letter_score.set_position((j + 0.85, i+ 0.15))
                                   self.letter_score.set_text(self.tile_board[i, j].score)
                                   self.rect.set_xy((j, i))
                                   self.ax.draw_artist(self.rect)
                                   self.ax.draw_artist(self.letter_score)
                                   self.ax.draw_artist(self.letter)
                              index += 1
                    self.background = self.canvas.copy_from_bbox(self.ax.bbox)
                    for i in range(index, len(lines)):
                         l = lines[i].strip()
                         self.bag.tiles.append(Tile(l[0], int(l[1:])))
                    self.bag.tiles_left = len(self.bag.tiles)
          self.create_widgets()
     def create_widgets(self):
          self.is_first_turn = True
          self.fig, self.ax = plt.subplots(figsize=(9, 9))
          self.ax.set_aspect("equal")
          self.ax.set_xlim(0, 15)
          self.ax.set_ylim(-1, 15)
          self.ax.axis("off")
          for i in range(15):
               for j in range(15):
                    if(letter_multiplier[i, j] == 2): 
                         self.ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='lightskyblue', edgecolor="white"))
                         self.ax.text(j + 0.5, i + 0.5, 'LETTRE\nCOMPTE\nDOUBLE', ha="center", va="center", fontsize=5, color="black")
                    elif(letter_multiplier[i, j] == 3): 
                         self.ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='dodgerblue', edgecolor="white"))
                         self.ax.text(j + 0.5, i + 0.5, 'LETTRE\nCOMPTE\nTRIPLE', ha="center", va="center", fontsize=5, color="black")
                    elif(word_score[i, j] == 2): 
                         self.ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='tomato', edgecolor="white"))
                         if(i != 7 != j): self.ax.text(j + 0.5, i + 0.5, 'MOT\nCOMPTE\nDOUBLE', ha="center", va="center", fontsize=5, color="black")
                    elif(word_score[i, j] == 3): 
                         self.ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='red', edgecolor="white"))
                         self.ax.text(j + 0.5, i + 0.5, 'MOT\nCOMPTE\nTRIPLE', ha="center", va="center", fontsize=5, color="black")
                    else: 
                         self.ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='tan', edgecolor="white"))
          self.ax.plot(7.5, 7.5, '*', markersize = 22, color = 'black')

          self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
          self.canvas.draw()
          self.canvas.get_tk_widget().grid(row=0, column=0, pady=(10,10))


          self.background = self.canvas.copy_from_bbox(self.ax.bbox)
          self.selected = plt.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black')
          self.rect = plt.Rectangle((0, 0), 1, 1, facecolor = 'bisque', edgecolor = 'black')
          self.ax.add_patch(self.selected)
          self.ax.add_patch(self.rect)
          self.letter = self.ax.text(0.5, 0.5, '', ha="center", va="center", fontsize=14, color="black")
          self.letter_score = self.ax.text(0.35, 0.35, '', ha="center", va="center", fontsize=5, color="black")

          self.fig.canvas.mpl_connect("motion_notify_event", self.on_move)
          self.fig.canvas.mpl_connect("button_press_event", self.on_click)
          self.fig.canvas.mpl_connect("button_release_event", self.on_release)
          self.fig.canvas.mpl_connect("key_press_event", self.key_press)

          self.score_labels = (ctk.CTkLabel(self, text = f"Score du joueur 1 : {self.players[0].score}"), ctk.CTkLabel(self, text = f"Score du joueur 2 : {self.players[1].score}"))
          self.score_labels[self.current_player].configure(text_color = 'red')
          self.score_labels[0].place(x=0, y=0)
          self.score_labels[1].place(x=0, y=20)

          self.draw_board()

          
     def on_click(self, event):
          if event.inaxes:
               x = int(event.xdata)
               y = int(event.ydata)
               if event.ydata < 0 and 4 <= x < len(self.players[self.current_player].hand) + 4:
                    self.selected_tile = self.players[self.current_player].hand[x - 4]
                    self.players[self.current_player].hand.pop(x - 4)
               elif 0 <= y < 15 and 0 <= x < 15 and self.is_new[y, x]:
                    self.selected_tile = self.tile_board[y, x]
                    self.tile_board[y, x] = None
                    self.is_new[y, x] = False
               self.draw_board(event)

     def draw_board(self, event = None):
          self.fig.canvas.restore_region(self.background)
          for i, tile in enumerate(self.players[self.current_player].hand):
               x = 4 + i + int(self.selected_tile != None and event.ydata < 0 and event.xdata < i + 4 + 0.5)
               self.letter.set_position((x + 0.5, -0.5))
               self.letter_score.set_position((x + 0.85, -0.85))
               self.rect.set_xy((x, -1))
               self.letter.set_text(tile.symbol)
               self.letter_score.set_text(tile.score)
               self.ax.draw_artist(self.rect)
               self.ax.draw_artist(self.letter_score)
               self.ax.draw_artist(self.letter)
          for i, row in enumerate(self.tile_board):
               for j, tile in enumerate(row):
                    if(self.is_new[i, j]):
                         self.letter.set_position((j + 0.5, i + 0.5))
                         self.letter.set_text(tile.symbol)
                         self.letter_score.set_position((j + 0.85, i+ 0.15))
                         self.letter_score.set_text(tile.score)
                         self.rect.set_xy((j, i))
                         self.ax.draw_artist(self.rect)
                         self.ax.draw_artist(self.letter_score)
                         self.ax.draw_artist(self.letter)
          if self.selected_tile and event.inaxes:
               self.letter.set_position((event.xdata, event.ydata))
               self.letter.set_text(self.selected_tile.symbol)
               self.letter_score.set_position((event.xdata + 0.35, event.ydata - 0.35))
               self.letter_score.set_text(self.selected_tile.score)
               self.rect.set_xy((event.xdata - 0.5, event.ydata - 0.5))
               if event.ydata >= 0 :
                    self.selected.set_visible(True)
                    self.selected.set_xy((int(event.xdata), int(event.ydata)))
                    self.ax.draw_artist(self.selected)
                    self.selected.set_visible(False)
               self.ax.draw_artist(self.rect)
               self.ax.draw_artist(self.letter_score)
               self.ax.draw_artist(self.letter)
               
          self.fig.canvas.blit(self.ax.bbox)

     def on_release(self, event):
          if self.selected_tile:
               if event.inaxes:
                    x = int(event.xdata)
                    y = int(event.ydata)
                    if 0 <= event.ydata and not self.tile_board[y, x]:
                         self.is_new[y, x] = True
                         self.tile_board[y, x] = self.selected_tile
                    else: self.players[self.current_player].hand.insert(max(0, min( int(event.xdata - 3.5), len(self.players[self.current_player].hand))), self.selected_tile) #repositionning hand tiles
               else: self.players[self.current_player].hand.append(self.selected_tile)
               self.selected_tile = None
               self.canvas.restore_region(self.background)
               self.draw_board(event)
               self.canvas.blit(self.ax.bbox)

     def key_press(self, event):
          if event.key == 'enter':
               score = self.calc_score()
               if score:
                    self.fig.canvas.restore_region(self.background)
                    for i, row in enumerate(self.tile_board):
                         for j, tile in enumerate(row):
                              if(self.is_new[i, j]):
                                   self.is_new[i, j] = False
                                   self.letter.set_position((j + 0.5, i + 0.5))
                                   self.letter.set_text(tile.symbol)
                                   self.letter_score.set_position((j + 0.85, i+ 0.15))
                                   self.letter_score.set_text(tile.score)
                                   self.rect.set_xy((j, i))
                                   self.ax.draw_artist(self.rect)
                                   self.ax.draw_artist(self.letter_score)
                                   self.ax.draw_artist(self.letter)
                    self.background = self.canvas.copy_from_bbox(self.ax.bbox) # rend les tuiles impregnier dans lecran
                    self.players[self.current_player].draw_tiles()
                    self.players[self.current_player].score += score
                    self.score_labels[self.current_player].configure(text = f"Score du joueur {self.current_player + 1} : {self.players[self.current_player].score}", text_color = 'black')
                    self.current_player = not self.current_player
                    self.score_labels[self.current_player].configure(text_color = 'red')
                    self.is_first_turn = False
                    self.draw_board()
          elif event.key == 's':
               self.save_game("game.txt")

     def save_game(self, file_name):
          for i in range(0, 15):
               for j in range(0, 15):
                    if self.is_new[i, j]:
                         self.is_new[i, j] = False
                         self.players[self.current_player].hand.append(self.tile_board[i, j])
                         self.tile_board[i, j] = None
          with open(file_name, 'w') as file:
               file.write(f"{self.current_player}\n")
               file.write(f"{self.players[0].score}\n")
               file.write(f"{self.players[1].score}\n")
               file.write(f"{self.is_first_turn}\n")
               for player in self.players:
                    for tile in player.hand:
                         file.write(f"{tile.symbol}{tile.score}\n")
                    file.write('\n')
               for i in range(0, 15):
                    for j in range(0, 15):
                         if self.tile_board[i, j] != None: file.write(f"{self.tile_board[i, j].symbol}{self.tile_board[i, j].score}\n")
                         else: file.write('\n')
               for tile in self.bag.tiles:
                    file.write(f"{tile.symbol}{tile.score}\n")


          

     def on_move(self, event):
          if self.selected_tile and event.inaxes:
               self.canvas.restore_region(self.background)
               self.draw_board(event)
               self.canvas.blit(self.ax.bbox)

     def calc_score(self):
          tiles_placed = self.players[self.current_player].hand_max_size - len(self.players[self.current_player].hand)
          for i in range(14, 0, -1):
               for j in range(0, 15): 
                    if self.is_new[i, j]:
                         total_score = 0
                         isConnected = False

                         horizontal_num = 0
                         xs = j + 1
                         while xs < 15 and self.tile_board[i, xs]:
                              horizontal_num += self.is_new[i, xs]
                              xs += 1
                         if 0 < horizontal_num < tiles_placed - 1: return False #on regardes si toutes les tuiles placees sont dans le meme axe
                         
                         vertical_num = 0
                         ys = j + 1
                         while ys < 15 and self.tile_board[ys, j]:
                              vertical_num += self.is_new[ys, j]
                              ys += 1
                         if 0 < vertical_num < tiles_placed - 1: return False
                         
                         if horizontal_num:
                              current_score = 0
                              current_word = []
                              word_multiplier = 1
                              ys, xs = i, j
                              while xs > 0 and self.tile_board[ys, xs - 1]: xs -= 1 # find the start of the word, can be made faster if use same strat as intersect word, but this is cleaner
                              while xs < 15 and self.tile_board[ys, xs]: # read the word
                                   current_word.append(self.tile_board[ys, xs].symbol)
                                   if self.is_new[ys, xs]:
                                        word_multiplier *= word_score[ys, xs]
                                        current_score += self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                        if (ys < 14 and self.tile_board[ys + 1, xs]) or (ys > 0 and self.tile_board[ys - 1, xs]):
                                             isConnected = True
                                             intersecting_score = self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                             intersecting_word = []
                                             y = ys + 1
                                             while y < 15 and self.tile_board[y, xs]:
                                                  intersecting_word += self.tile_board[y, xs].symbol
                                                  intersecting_score += self.tile_board[y, xs].score
                                                  y += 1
                                             intersecting_word = intersecting_word[::-1] + [self.tile_board[ys, xs].symbol]
                                             y = ys - 1
                                             while y >= 0 and self.tile_board[y, xs]:
                                                  intersecting_word += self.tile_board[y, xs].symbol
                                                  intersecting_score += self.tile_board[y, xs].score
                                                  y -= 1
                                             if Dictionary().is_word_valid(tuple(intersecting_word)): total_score += intersecting_score * word_score[ys, xs]
                                             else: return False
                                   else:
                                        isConnected = True
                                        current_score += self.tile_board[ys, xs].score # pas besoin de regarder si un mot intersecte
                                   xs += 1
                              if Dictionary().is_word_valid(tuple(current_word)): total_score += current_score * word_multiplier
                              else: return False

                         elif vertical_num:
                              current_score = 0
                              current_word = []
                              word_multiplier = 1
                              ys, xs = i, j
                              while ys < 14 and self.tile_board[ys + 1, xs]: ys += 1 # find the start of the word
                              while ys >= 0 and self.tile_board[ys, xs]: # read the word
                                   current_word.append(self.tile_board[ys, xs].symbol)
                                   if self.is_new[ys, xs]:
                                        word_multiplier *= word_score[ys, xs]
                                        current_score += self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                        if (xs < 14 and self.tile_board[ys, xs + 1]) or (xs > 0 and self.tile_board[ys, xs - 1]):
                                             isConnected = True
                                             intersecting_score = self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                             intersecting_word = []
                                             x = xs - 1
                                             while x >= 0 and self.tile_board[ys, x]:
                                                  intersecting_word += self.tile_board[ys, x].symbol
                                                  intersecting_score += self.tile_board[ys, x].score
                                                  x -= 1
                                             intersecting_word = intersecting_word[::-1] + [self.tile_board[ys, xs].symbol]
                                             x = xs + 1
                                             while x < 15 and self.tile_board[ys, x]:
                                                  intersecting_word += self.tile_board[ys, x].symbol
                                                  intersecting_score += self.tile_board[ys, x].score
                                                  x += 1
                                             if Dictionary().is_word_valid(tuple(intersecting_word)): total_score += intersecting_score * word_score[ys, xs]
                                             else: return False
                                   else:
                                        isConnected = True
                                        current_score += self.tile_board[ys, xs].score # pas besoin de regarder si un mot intersecte
                                   ys -= 1
                              if Dictionary().is_word_valid(tuple(current_word)): total_score += current_score * word_multiplier
                              else: return False
                         else: #placed a single tile, so we will only check how others intersect with it, maybe put the intersection in functions, we repeat a lot...
                              ys, xs = i, j
                              if (xs < 14 and self.tile_board[ys, xs + 1]) or (xs > 0 and self.tile_board[ys, xs - 1]):
                                   isConnected = True
                                   intersecting_score = self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                   intersecting_word = []
                                   x = xs - 1
                                   while x >= 0 and self.tile_board[ys, x]:
                                        intersecting_word += self.tile_board[ys, x].symbol
                                        intersecting_score += self.tile_board[ys, x].score
                                        x -= 1
                                   intersecting_word = intersecting_word[::-1] + [self.tile_board[ys, xs].symbol]
                                   x = xs + 1
                                   while x < 15 and self.tile_board[ys, x]:
                                        intersecting_word += self.tile_board[ys, x].symbol
                                        intersecting_score += self.tile_board[ys, x].score
                                        x += 1
                                   if Dictionary().is_word_valid(tuple(intersecting_word)): total_score += intersecting_score * word_score[ys, xs]
                                   else: return False

                              if (ys < 14 and self.tile_board[ys + 1, xs]) or (ys > 0 and self.tile_board[ys - 1, xs]):
                                   isConnected = True
                                   intersecting_score = self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                   intersecting_word = []
                                   y = ys + 1
                                   while y < 15 and self.tile_board[y, xs]:
                                        intersecting_word += self.tile_board[y, xs].symbol
                                        intersecting_score += self.tile_board[y, xs].score
                                        y += 1
                                   intersecting_word = intersecting_word[::-1] + [self.tile_board[ys, xs].symbol]
                                   y = ys - 1
                                   while y >= 0 and self.tile_board[y, xs]:
                                        intersecting_word += self.tile_board[y, xs].symbol
                                        intersecting_score += self.tile_board[y, xs].score
                                        y -= 1
                                   if Dictionary().is_word_valid(tuple(intersecting_word)): total_score += intersecting_score * word_score[ys, xs]
                                   else: return False
                         if tiles_placed == 7: total_score += 50
                         if isConnected or (self.is_first_turn and self.is_new[7, 7]): return total_score
                         return False