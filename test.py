import matplotlib.pyplot as plt
import numpy as np
from Bag import Tile
from Bag import Player
from Bag import Bag
import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
     def __init__(self, master=None):
          super().__init__(master)
          self.master = master
          self.create_widgets()
     def create_widgets(self):
          self.fig, self.ax = plt.subplots()
          self.ax.set_aspect("equal")
          self.ax.set_xlim(0, 15)
          self.ax.set_ylim(-1, 15)
          self.ax.axis("off") #Note for later : font size will have to adapt to the size of the window
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
          self.canvas.get_tk_widget().grid(row=2, column=0, pady=(10,10))


          self.background = self.canvas.copy_from_bbox(self.ax.bbox)
          self.selected = plt.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', visible = False)
          self.rect = plt.Rectangle((0, 0), 1, 1, facecolor = 'bisque', edgecolor = 'black', visible = False)
          self.ax.add_patch(self.selected)
          self.ax.add_patch(self.rect)
          self.letter = self.ax.text(0.5, 0.5, '', ha="center", va="center", fontsize=14, color="black", visible = False)
          self.letter_score = self.ax.text(0.35, 0.35, '', ha="center", va="center", fontsize=5, color="black", visible = False)

          self.bag = Bag()
          self.players = (Player(self.bag, ""), Player(self.bag, ""))
          self.current_player = False
          self.tile_board = np.full((15, 15), None)
          self.is_new = np.zeros((15, 15))

          self.selected_tile = None
          self.fig.canvas.mpl_connect("draw_event", self.on_draw)
          self.fig.canvas.mpl_connect("motion_notify_event", self.on_move)
          self.fig.canvas.mpl_connect("button_press_event", self.on_click)
          self.fig.canvas.mpl_connect("button_release_event", self.on_release)
          self.fig.canvas.mpl_connect("key_press_event", self.key_press)

          self.dic = set()
          with open("French ODS dictionary.txt", 'r') as f: #temporary
               for i in f:
                    self.dic.add(tuple(i[:-1]))
          
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

     def draw_board(self, event):
          self.letter_score.set_visible(True) #maybe remove if no resizes
          self.letter.set_visible(True)
          self.rect.set_visible(True)
          self.fig.canvas.restore_region(self.background)
          for i, tile in enumerate(self.players[self.current_player].hand):
               x = int(self.selected_tile != None and event.ydata < 0 and event.xdata < i + 4 + 0.5) + 4 + i#error but idk why
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
          if event.inaxes and self.selected_tile:
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
               
          self.letter_score.set_visible(False)
          self.letter.set_visible(False)
          self.rect.set_visible(False)
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
                    self.letter_score.set_visible(True) #maybe remove if no resizes
                    self.letter.set_visible(True)
                    self.rect.set_visible(True)
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
                    self.letter_score.set_visible(False)
                    self.letter.set_visible(False)
                    self.rect.set_visible(False)
                    self.background = self.canvas.copy_from_bbox(self.ax.bbox) # rend les tuiles impregnier dans lecran
                    self.players[self.current_player].draw_tiles()
                    self.players[self.current_player].score += score
                    print(score)
                    print(self.bag.tiles)
                    self.current_player = not self.current_player
               else: print("Invalid Word!")




     def on_draw(self, event): #for resize
          background = self.canvas.copy_from_bbox(self.ax.bbox)

     def on_move(self, event):
          if self.selected_tile:
               self.canvas.restore_region(self.background)
               self.draw_board(event)
               self.canvas.blit(self.ax.bbox)


     def calc_score(self): # add the +50 point when 7 tiles are used
          tiles_in_axis = 0
          for i in range(14, 0, -1): 
               for j in range(0, 15): 
                    if self.is_new[i, j]:
                         total_score = 0
                         isConnected = False
                         horizontal_read = j < 15 and self.is_new[i, j + 1]
                         vertical_read = i >= 0 and self.is_new[i - 1, j]
                         if horizontal_read:
                              current_score = 0
                              current_word = []
                              word_multiplier = 1
                              ys, xs = i, j
                              while xs > 0 and self.tile_board[ys, xs - 1]: xs -= 1 # find the start of the word, can be made faster if use same strat as intersect word, but this is cleaner
                              while xs < 15 and self.tile_board[ys, xs]: # read the word
                                   current_word += self.tile_board[ys, xs].symbol
                                   if self.is_new[ys, xs]:
                                        tiles_in_axis += 1
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
                                             if tuple(intersecting_word) in self.dic: total_score += intersecting_score * word_score[ys, xs]
                                             else: return False
                                   else:
                                        current_score += self.tile_board[ys, xs].score # pas besoin de regarder si un mot intersecte
                                   xs += 1
                              if tuple(current_word) in self.dic: total_score += current_score * word_multiplier
                              else: return False

                         elif vertical_read:
                              current_score = 0
                              current_word = []
                              word_multiplier = 1
                              ys, xs = i, j
                              while ys < 14 and self.tile_board[ys + 1, xs]: ys += 1 # find the start of the word
                              while ys >= 0 and self.tile_board[ys, xs]: # read the word
                                   current_word += self.tile_board[ys, xs].symbol
                                   if self.is_new[ys, xs]:
                                        tiles_in_axis += 1
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
                                             if tuple(intersecting_word) in self.dic: total_score += intersecting_score * word_score[ys, xs]
                                             else: return False
                                   else:
                                        current_score += self.tile_board[ys, xs].score # pas besoin de regarder si un mot intersecte
                                   ys -= 1
                              if tuple(current_word) in self.dic: total_score += current_score * word_multiplier
                              else: return False
                         else: #placed a single tile, so we will only check how others intersect with it, maybe put the intersection in functions, we repeat a lot...
                              tiles_in_axis = 1
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
                                   if tuple(intersecting_word) in self.dic: total_score += intersecting_score * word_score[ys, xs]
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
                                   if tuple(intersecting_word) in self.dic: total_score += intersecting_score * word_score[ys, xs]
                                   else: return False

                         if True: #and isConnected
                              if tiles_in_axis == 7-len(self.players[self.current_player].hand):
                                   return total_score
                         return False