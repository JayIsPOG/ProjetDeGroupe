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
     [2 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,2 ,],
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
ax = plt.subplot()
ax.set_aspect("equal")
ax.set_xlim(0, 15)
ax.set_ylim(0, 15)
ax.axis("off") #Note for later : font size will have to adapt to the size of the window
for i in range(15):
    for j in range(15):
        if(letter_score[i, j] == 2): 
             ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='lightskyblue', edgecolor="white"))
             ax.text(j + 0.5, i + 0.5, 'DOUBLE\nLETTER\nSCORE', ha="center", va="center", fontsize=5, color="black")
        elif(letter_score[i, j] == 3): 
             ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='dodgerblue', edgecolor="white"))
             ax.text(j + 0.5, i + 0.5, 'TRIPLE\nLETTER\nSCORE', ha="center", va="center", fontsize=5, color="black")
        elif(word_score[i, j] == 1): 
             ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='tomato', edgecolor="white"))
             ax.text(j + 0.5, i + 0.5, 'DOUBLE\nWORD\nSCORE', ha="center", va="center", fontsize=5, color="black")
        elif(word_score[i, j] == 2): 
             ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='red', edgecolor="white"))
             ax.text(j + 0.5, i + 0.5, 'TRIPLE\nWORD\nSCORE', ha="center", va="center", fontsize=5, color="black")
        else: 
             ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='tan', edgecolor="white"))
ax.add_patch(plt.Rectangle((7, 7), 1, 1,facecolor='tomato', edgecolor="white"))
ax.plot(7.5, 7.5, '*', markersize = 22, color = 'black')
def on_mouse_move(event):
        if event.inaxes:  # Check if the cursor is within the axes
            print((int(event.xdata), int(event.ydata)))
plt.connect('motion_notify_event',on_mouse_move)
plt.show()

for i in word_score:
     print('[', end = '')
     for j in i:
          print(j - 11, ',', end = '')
     print('],')
        