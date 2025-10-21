import matplotlib.pyplot as plt
import numpy as np
from Bag import Tile
from Bag import Player
from Bag import Bag
import customtkinter as ctk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class Scrabble(ctk.CTkFrame):
     def __init__(self, master=None):
          super().__init__(master)
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
          
     def on_click(self, event):
          global selected_tile
          if event.inaxes:
               x = int(event.xdata)
               y = int(event.ydata)
               if event.ydata < 0 and 4 <= x < len(self.player.hand) + 4:
                    selected_tile = player.hand[x - 4]
                    player.hand.pop(x - 4)
               elif 0 <= y < 15 and 0 <= x < 15 and is_new[y, x]:
                    selected_tile = tile_board[y, x]
                    tile_board[y, x] = None
                    is_new[y, x] = False
               draw_board(event)

     def draw_board(self, event):
          letter_score.set_visible(True) #maybe remove if no resizes
          letter.set_visible(True)
          rect.set_visible(True)
          fig.canvas.restore_region(background)
          for i, tile in enumerate(player.hand):
               x = int(selected_tile != None and event.ydata < 0 and event.xdata < i + 4 + 0.5) + 4 + i#error but idk why
               letter.set_position((x + 0.5, -0.5))
               letter_score.set_position((x + 0.85, -0.85))
               rect.set_xy((x, -1))
               letter.set_text(tile.symbol)
               letter_score.set_text(tile.score)
               ax.draw_artist(rect)
               ax.draw_artist(letter_score)
               ax.draw_artist(letter)
          for i, row in enumerate(tile_board):
               for j, tile in enumerate(row):
                    if(is_new[i, j]):
                         letter.set_position((j + 0.5, i + 0.5))
                         letter.set_text(tile.symbol)
                         letter_score.set_position((j + 0.85, i+ 0.15))
                         letter_score.set_text(tile.score)
                         rect.set_xy((j, i))
                         ax.draw_artist(rect)
                         ax.draw_artist(letter_score)
                         ax.draw_artist(letter)
          if event.inaxes and selected_tile:
               letter.set_position((event.xdata, event.ydata))
               letter.set_text(selected_tile.symbol)
               letter_score.set_position((event.xdata + 0.35, event.ydata - 0.35))
               letter_score.set_text(selected_tile.score)
               rect.set_xy((event.xdata - 0.5, event.ydata - 0.5))
               if event.ydata >= 0 :
                    selected.set_visible(True)
                    selected.set_xy((int(event.xdata), int(event.ydata)))
                    ax.draw_artist(selected)
                    selected.set_visible(False)
               ax.draw_artist(rect)
               ax.draw_artist(letter_score)
               ax.draw_artist(letter)
               
          letter_score.set_visible(False)
          letter.set_visible(False)
          rect.set_visible(False)
          fig.canvas.blit(ax.bbox)


     def on_release(self, event):
          global selected_tile
          if selected_tile:
               if event.inaxes:
                    x = int(event.xdata)
                    y = int(event.ydata)
                    if 0 <= event.ydata and not tile_board[y, x]:
                         is_new[y, x] = True
                         tile_board[y, x] = selected_tile
                    else: player.hand.insert(max(0, min( int(event.xdata - 3.5), len(player.hand))), selected_tile) #repositionning hand tiles
               else: player.hand.append(selected_tile)
               selected_tile = None
               canvas.restore_region(background)
               draw_board(event)
               canvas.blit(ax.bbox)

     def key_press(self, event):
          if event.key == 'enter':
               score = calc_score(7-len(player.hand))
               if score:
                    global background
                    letter_score.set_visible(True) #maybe remove if no resizes
                    letter.set_visible(True)
                    rect.set_visible(True)
                    fig.canvas.restore_region(background)
                    for i, row in enumerate(tile_board):
                         for j, tile in enumerate(row):
                              if(is_new[i, j]):
                                   is_new[i, j] = False
                                   letter.set_position((j + 0.5, i + 0.5))
                                   letter.set_text(tile.symbol)
                                   letter_score.set_position((j + 0.85, i+ 0.15))
                                   letter_score.set_text(tile.score)
                                   rect.set_xy((j, i))
                                   ax.draw_artist(rect)
                                   ax.draw_artist(letter_score)
                                   ax.draw_artist(letter)
                    letter_score.set_visible(False)
                    letter.set_visible(False)
                    rect.set_visible(False)
                    background = canvas.copy_from_bbox(ax.bbox) # rend les tuiles impregnier dans lecran
                    player.draw_tiles()
                    player.score += score
                    print(score)
                    print(bag.tiles)
               else: print("Invalid Word!")




     def on_draw(self, event): #for resize
     global background
     background = canvas.copy_from_bbox(ax.bbox)

     def on_move(event):
          if selected_tile:
               canvas.restore_region(background)
               draw_board(event)
               canvas.blit(ax.bbox)

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

dic = set()
with open("French ODS dictionary.txt", 'r') as f: #temporary
     for i in f:
          dic.add(tuple(i[:-1]))

def calc_score(num_tiles_placed): # add the +50 point when 7 tiles are used
     tiles_in_axis = 0
     for i in range(14, 0, -1): 
          for j in range(0, 15): 
               if is_new[i, j]:
                    total_score = 0
                    isConnected = False
                    horizontal_read = j < 15 and is_new[i, j + 1]
                    vertical_read = i >= 0 and is_new[i - 1, j]
                    if horizontal_read:
                         current_score = 0
                         current_word = []
                         word_multiplier = 1
                         ys, xs = i, j
                         while xs > 0 and tile_board[ys, xs - 1]: xs -= 1 # find the start of the word, can be made faster if use same strat as intersect word, but this is cleaner
                         while xs < 15 and tile_board[ys, xs]: # read the word
                              current_word += tile_board[ys, xs].symbol
                              if is_new[ys, xs]:
                                   tiles_in_axis += 1
                                   word_multiplier *= word_score[ys, xs]
                                   current_score += tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                   if (ys < 14 and tile_board[ys + 1, xs]) or (ys > 0 and tile_board[ys - 1, xs]):
                                        isConnected = True
                                        intersecting_score = tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                        intersecting_word = []
                                        y = ys + 1
                                        while y < 15 and tile_board[y, xs]:
                                             intersecting_word += tile_board[y, xs].symbol
                                             intersecting_score += tile_board[y, xs].score
                                             y += 1
                                        intersecting_word = intersecting_word[::-1] + [tile_board[ys, xs].symbol]
                                        y = ys - 1
                                        while y >= 0 and tile_board[y, xs]:
                                             intersecting_word += tile_board[y, xs].symbol
                                             intersecting_score += tile_board[y, xs].score
                                             y -= 1
                                        if tuple(intersecting_word) in dic: total_score += intersecting_score * word_score[ys, xs]
                                        else: return False
                              else:
                                   current_score += tile_board[ys, xs].score # pas besoin de regarder si un mot intersecte
                              xs += 1
                         if tuple(current_word) in dic: total_score += current_score * word_multiplier
                         else: return False

                    elif vertical_read:
                         current_score = 0
                         current_word = []
                         word_multiplier = 1
                         ys, xs = i, j
                         while ys < 14 and tile_board[ys + 1, xs]: ys += 1 # find the start of the word
                         while ys >= 0 and tile_board[ys, xs]: # read the word
                              current_word += tile_board[ys, xs].symbol
                              if is_new[ys, xs]:
                                   tiles_in_axis += 1
                                   word_multiplier *= word_score[ys, xs]
                                   current_score += tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                   if (xs < 14 and tile_board[ys, xs + 1]) or (xs > 0 and tile_board[ys, xs - 1]):
                                        isConnected = True
                                        intersecting_score = tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                        intersecting_word = []
                                        x = xs - 1
                                        while x >= 0 and tile_board[ys, x]:
                                             intersecting_word += tile_board[ys, x].symbol
                                             intersecting_score += tile_board[ys, x].score
                                             x -= 1
                                        intersecting_word = intersecting_word[::-1] + [tile_board[ys, xs].symbol]
                                        x = xs + 1
                                        while x < 15 and tile_board[ys, x]:
                                             intersecting_word += tile_board[ys, x].symbol
                                             intersecting_score += tile_board[ys, x].score
                                             x += 1
                                        if tuple(intersecting_word) in dic: total_score += intersecting_score * word_score[ys, xs]
                                        else: return False
                              else:
                                   current_score += tile_board[ys, xs].score # pas besoin de regarder si un mot intersecte
                              ys -= 1
                         if tuple(current_word) in dic: total_score += current_score * word_multiplier
                         else: return False
                    else: #placed a single tile, so we will only check how others intersect with it, maybe put the intersection in functions, we repeat a lot...
                         tiles_in_axis = 1
                         ys, xs = i, j
                         if (xs < 14 and tile_board[ys, xs + 1]) or (xs > 0 and tile_board[ys, xs - 1]):
                              isConnected = True
                              intersecting_score = tile_board[ys, xs].score * letter_multiplier[ys, xs]
                              intersecting_word = []
                              x = xs - 1
                              while x >= 0 and tile_board[ys, x]:
                                   intersecting_word += tile_board[ys, x].symbol
                                   intersecting_score += tile_board[ys, x].score
                                   x -= 1
                              intersecting_word = intersecting_word[::-1] + [tile_board[ys, xs].symbol]
                              x = xs + 1
                              while x < 15 and tile_board[ys, x]:
                                   intersecting_word += tile_board[ys, x].symbol
                                   intersecting_score += tile_board[ys, x].score
                                   x += 1
                              if tuple(intersecting_word) in dic: total_score += intersecting_score * word_score[ys, xs]
                              else: return False

                         if (ys < 14 and tile_board[ys + 1, xs]) or (ys > 0 and tile_board[ys - 1, xs]):
                              isConnected = True
                              intersecting_score = tile_board[ys, xs].score * letter_multiplier[ys, xs]
                              intersecting_word = []
                              y = ys + 1
                              while y < 15 and tile_board[y, xs]:
                                   intersecting_word += tile_board[y, xs].symbol
                                   intersecting_score += tile_board[y, xs].score
                                   y += 1
                              intersecting_word = intersecting_word[::-1] + [tile_board[ys, xs].symbol]
                              y = ys - 1
                              while y >= 0 and tile_board[y, xs]:
                                   intersecting_word += tile_board[y, xs].symbol
                                   intersecting_score += tile_board[y, xs].score
                                   y -= 1
                              if tuple(intersecting_word) in dic: total_score += intersecting_score * word_score[ys, xs]
                              else: return False

                    if True: #and isConnected
                         if tiles_in_axis == num_tiles_placed:
                              return total_score
                    return False


     
plt.show()