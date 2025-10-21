import matplotlib.pyplot as plt
import numpy as np
class JeuScrabble():
     def __init__(self):
          pass
     def joue():
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
          letter_score = np.array([
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
          fig, ax = plt.subplots()
          ax.set_aspect("equal")
          ax.set_xlim(0, 15)
          ax.set_ylim(-1, 15)
          ax.axis("off") #Note for later : font size will have to adapt to the size of the window
          for i in range(15):
              for j in range(15):
                  if(letter_score[i, j] == 2): 
                       ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='lightskyblue', edgecolor="white"))
                       ax.text(j + 0.5, i + 0.5, 'LETTRE\nCOMPTE\nDOUBLE', ha="center", va="center", fontsize=5, color="black")
                  elif(letter_score[i, j] == 3): 
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

          class Tile:
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
               letter.set_y(-0.5)
               letter_score.set_y(-0.85)
               rect.set_y(-1)
               for i, tile in enumerate(hand_tiles):
                    dx = int(selected_tile != None and event.ydata < 0 and event.xdata < i + 4 + 0.5) + 4 #error but idk why
                    rect.set_x(i + dx)
                    letter.set_x(0.5 + i + dx)
                    letter.set_text(tile.symbol)
                    letter_score.set_x(0.85 + i + dx)
                    letter_score.set_text(tile.score)
                    ax.draw_artist(rect)
                    ax.draw_artist(letter)
                    ax.draw_artist(letter_score)
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
                    selected.set_visible(True)
                    letter.set_position((event.xdata, event.ydata))
                    letter.set_text(selected_tile.symbol)
                    letter_score.set_position((event.xdata + 0.35, event.ydata - 0.35))
                    letter_score.set_text(selected_tile.score)
                    rect.set_xy((event.xdata - 0.5, event.ydata - 0.5))
                    selected.set_xy((int(event.xdata), int(event.ydata)))
                    ax.draw_artist(selected)
                    ax.draw_artist(rect)
                    ax.draw_artist(letter_score)
                    ax.draw_artist(letter)
                    selected.set_visible(False)
               letter_score.set_visible(False)
               letter.set_visible(False)
               rect.set_visible(False)

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
          plt.show()