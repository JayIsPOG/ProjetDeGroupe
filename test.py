import matplotlib.pyplot as plt
import numpy as np
word_score = np.array([
     [2 ,0 ,0 ,0 ,0 ,0 ,0 ,2 ,0 ,0 ,0 ,0 ,0 ,0 ,2 ,],
     [0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,],
     [0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,],
     [0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,],
     [0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,],
     [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,],
     [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,],
     [2 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,2 ,],
     [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,],
     [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,],
     [0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,],
     [0 ,0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,0 ,],
     [0 ,0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,0 ,],
     [0 ,1 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,1 ,0 ,],
     [2 ,0 ,0 ,0 ,0 ,0 ,0 ,2 ,0 ,0 ,0 ,0 ,0 ,0 ,2 ,],
        ])
letterScore = np.array([
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
print(letterScore[0, 0])
fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.set_xlim(0, 15)
ax.set_ylim(-1, 15)
ax.axis("off") #Note for later : font size will have to adapt to the size of the window
for i in range(15):
    for j in range(15):
        if(letterScore[i, j] == 2): 
             ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='lightskyblue', edgecolor="white"))
             ax.text(j + 0.5, i + 0.5, 'LETTRE\nCOMPTE\nDOUBLE', ha="center", va="center", fontsize=5, color="black")
        elif(letterScore[i, j] == 3): 
             ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='dodgerblue', edgecolor="white"))
             ax.text(j + 0.5, i + 0.5, 'LETTRE\nCOMPTE\nTRIPLE', ha="center", va="center", fontsize=5, color="black")
        elif(word_score[i, j] == 1): 
             ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='tomato', edgecolor="white"))
             if(i != 7 != j): ax.text(j + 0.5, i + 0.5, 'MOT\nCOMPTE\nDOUBLE', ha="center", va="center", fontsize=5, color="black")
        elif(word_score[i, j] == 2): 
             ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='red', edgecolor="white"))
             ax.text(j + 0.5, i + 0.5, 'MOT\nCOMPTE\nTRIPLE', ha="center", va="center", fontsize=5, color="black")
        else: 
             ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='tan', edgecolor="white"))
ax.plot(7.5, 7.5, '*', markersize = 22, color = 'black')

class Tile: # a enlever
     def __init__(self, symbol, score):
          self.symbol = symbol
          self.score = score

canvas = fig.canvas
canvas.draw()
background = canvas.copy_from_bbox(ax.bbox)
selected = plt.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black', visible = False)
rect = plt.Rectangle((0, 0), 1, 1, facecolor = 'bisque', edgecolor = 'black', visible = False)
ax.add_patch(selected)
ax.add_patch(rect)
letter = ax.text(0.5, 0.5, '', ha="center", va="center", fontsize=14, color="black", visible = False)
letter_score = ax.text(0.35, 0.35, '', ha="center", va="center", fontsize=5, color="black", visible = False)

tile_board = np.full((15, 15), None)
is_new = np.zeros((15, 15))
hand_tiles = [Tile('A', 1), Tile('B', 2), Tile('C', 3), Tile('D', 4), Tile('E', 5), Tile('F', 6), Tile('G', 7)]
selected_tile = None


def on_click(event):
     global selected_tile
     if event.inaxes:
          x = int(event.xdata)
          y = int(event.ydata)
          if event.ydata < 0 and 4 <= x < len(hand_tiles) + 4:
               selected_tile = hand_tiles[x- 4]
               hand_tiles.pop(x - 4)
          elif 0 <= y < 15 and 0 <= x < 15:
               selected_tile = tile_board[y, x]
               tile_board[y, x] = None
               is_new[y, x] = False
          draw_board(event)

def draw_board(event):
     letter_score.set_visible(True) #maybe remove if no resizes
     letter.set_visible(True)
     rect.set_visible(True)
     fig.canvas.restore_region(background)
     for i, tile in enumerate(hand_tiles):
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


def on_release(event):
     global selected_tile
     if selected_tile:
          if event.inaxes:
               x = int(event.xdata)
               y = int(event.ydata)
               if 0 <= event.ydata and not tile_board[y, x]:
                    is_new[y, x] = True
                    tile_board[y, x] = selected_tile
               else: hand_tiles.insert(max(0, min( int(event.xdata - 3.5), len(hand_tiles))), selected_tile) #repositionning hand tiles
          else: hand_tiles.append(selected_tile)
          selected_tile = None
          canvas.restore_region(background)
          draw_board(event)
          canvas.blit(ax.bbox)
     print(calc_score())

def on_draw(event): #for resize
    global background
    background = canvas.copy_from_bbox(ax.bbox)

def on_move(event):
     if selected_tile:
          canvas.restore_region(background)
          draw_board(event)
          canvas.blit(ax.bbox)

fig.canvas.mpl_connect("draw_event", on_draw)
fig.canvas.mpl_connect("motion_notify_event", on_move)
fig.canvas.mpl_connect("button_press_event", on_click)
fig.canvas.mpl_connect("button_release_event", on_release)

def get_word_n_score(hpos, vpos, isHorizontal):
     score = 0
     word_mult = 0
     word = []
     if isHorizontal:
           while hpos < 15 and tile_board[vpos, hpos]:
                if is_new[vpos, hpos]:
                     word_mult += word_score[vpos, hpos]
                     score += letterScore[vpos, hpos] * tile_board[vpos, hpos].score
                else:
                     score += tile_board[vpos, hpos].score
                word.append(tile_board[vpos, hpos].symbol)
                hpos+=1
     else:
           while vpos < 15 and tile_board[vpos, hpos]:
                if is_new[vpos, hpos]:
                     word_mult += word_score[vpos, hpos]
                     score += letterScore[vpos, hpos] * tile_board[vpos, hpos].score
                else:
                     score += tile_board[vpos, hpos].score
                word.append(tile_board[vpos, hpos].symbol)
                vpos+=1
     if word_mult: return (score * word_mult, word)
     else: return (score, word)

dic = set()
with open("French ODS dictionary.txt", 'r') as f: #temporary
     for i in f:
          dic.add(tuple(i[:-1]))
def calc_score():
     for ystart in range(0, 15): 
          for xstart in range(0, 15): 
               if(is_new[ystart, xstart]):
                    currentScore = 0
                    if ystart > 0 and tile_board[ystart - 1, xstart]:
                         vpos = ystart - 1
                         while vpos >= 0 and tile_board[vpos, xstart]: vpos-=1
                         score, word = get_word_n_score(hpos, ystart, False)
                         currentScore += score
                         if not tuple(word) in dic: return False
                    elif ystart < 14 and tile_board[ystart + 1, xstart]:
                         score, word = get_word_n_score(xstart, ystart, False)
                         currentScore += score
                         if not tuple(word) in dic: return False
                    if xstart > 0 and tile_board[ystart, xstart - 1]:
                         hpos = xstart - 1
                         while hpos >= 0 and tile_board[ystart, hpos]: hpos-=1
                         score, word = get_word_n_score(hpos, ystart, True)
                         currentScore += score
                         if not tuple(word) in dic: return False
                    elif xstart < 14 and tile_board[ystart, xstart + 1]:
                         score, word = get_word_n_score(xstart, ystart, True)
                         currentScore += score
                         if not tuple(word) in dic: return False
                    if ystart < 14 and is_new[ystart + 1, xstart]: # lecture verticale
                         ystart += 1
                         while ystart < 15 and is_new[ystart, xstart]:
                              if xstart > 0 and tile_board[ystart, xstart - 1]:
                                   hpos = xstart - 1
                                   while hpos >= 0 and tile_board[ystart, hpos]: hpos-=1
                                   score, word = get_word_n_score(hpos, ystart, True)
                                   currentScore += score
                                   if not tuple(word) in dic: return False
                              elif xstart < 14 and tile_board[ystart, xstart + 1]:
                                   score, word = get_word_n_score(xstart, ystart, True)
                                   currentScore += score
                                   if not tuple(word) in dic: return False
                              ystart += 1
                    elif xstart < 14 and is_new[ystart, xstart + 1]: # lecture horizontale
                         xstart += 1
                         while xstart < 15 and is_new[ystart, xstart]:
                              if ystart > 0 and tile_board[ystart - 1, xstart]:
                                   vpos = ystart - 1
                                   while vpos >= 0 and tile_board[vpos, xstart]: vpos-=1
                                   score, word = get_word_n_score(hpos, ystart, False)
                                   currentScore += score
                                   if not tuple(word) in dic: return False
                              elif ystart < 14 and tile_board[ystart + 1, xstart]:
                                   score, word = get_word_n_score(xstart, ystart, False)
                                   currentScore += score
                                   if not tuple(word) in dic: return False
                              xstart += 1
                    return currentScore
     return 0



     
     
plt.show()