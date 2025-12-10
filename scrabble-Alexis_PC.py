import asyncio
import threading
import json
import websockets
import customtkinter as ctk
import matplotlib.pyplot as plt
import numpy as np
from Bag import Tile
from Bag import Player
from Bag import Bag
from dictionnaire import Dictionary
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

SERVER_IP = "ws://143.198.52.17:8765"

score_multiplier = np.array([
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

# ------------------------------
# PARTIE CLIENT-SERVEUR COMMENTÉE
# ------------------------------

SERVER_IP = "ws://165.227.38.141:8765"  # Adresse du serveur WebSocket Scrabble

class ScrabbleClient:
    def __init__(self, on_message_callback=None):
        self.ws = None               # WebSocket vers le serveur
        self.room_id = None          # Salle à laquelle le client appartient
        self.on_message = on_message_callback  # Fonction appelée dès qu’un message arrive
        self.loop = asyncio.new_event_loop()   # Boucle async dédiée (séparée du thread Tkinter)

        # Démarre la boucle asyncio dans un thread séparé → indispensable pour Tkinter + websockets
        t = threading.Thread(target=self._start_loop, args=(self.loop,), daemon=True)
        t.start()

    def _start_loop(self, loop):
        # Démarre la boucle async qui va gérer WebSocket en continu
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def _run(self, coro):
        # Permet d'exécuter une coroutine asyncio depuis le thread principal Tkinter
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    async def _connect(self):
        # Ouverture de la connexion WebSocket avec le serveur
        self.ws = await websockets.connect(SERVER_IP)
        print("Connecté au serveur")

    def connect(self):
        # Méthode publique → lance réellement la connexion
        return self._run(self._connect())


    # ---------- SALLES ----------
    async def _create_room(self, room):
        self.room_id = room
        if not self.ws:
            await self._connect()

        # Demande au serveur la création d'une salle
        await self.ws.send(json.dumps({"type": "create_room", "room": room}))

        # Attente confirmation serveur
        resp = json.loads(await self.ws.recv())

        # Démarre l’écoute des messages serveurs
        self._run(self._listen_forever())
        return resp

    def create_room(self, room):
        return self._run(self._create_room(room))


    async def _join_room(self, room):
        self.room_id = room
        if not self.ws:
            await self._connect()

        # Demande au serveur pour rejoindre une salle existante
        await self.ws.send(json.dumps({"type": "join_room", "room": room}))

        # Réponse du serveur
        resp = json.loads(await self.ws.recv())

        # Continue à écouter tout nouvel événement de jeu
        self._run(self._listen_forever())
        return resp

    def join_room(self, room):
        return self._run(self._join_room(room))


    # ---------- RÉCEPTION DES MESSAGES ----------
    async def _listen_forever(self):
        # Boucle infinie : écoute chaque message envoyé par le serveur
        try:
            async for msg in self.ws:
                try:
                    data = json.loads(msg)
                    # On appelle la fonction on_message fournie par GameWindow
                    if self.on_message:
                        self.on_message(json.dumps(data))
                except Exception as e:
                    print("Erreur traitement message:", e)
        except Exception as e:
            print("WebSocket stoppé:", e)


    # ---------- ENVOI D’UN MESSAGE ----------
    def send_raw(self, raw_json):
        # Permet d’envoyer un JSON brut au serveur
        if not self.ws:
            print("WebSocket pas encore connecté")
            return
        return self._run(self.ws.send(raw_json))


class GameWindow(ctk.CTk):
    def __init__(self, client: ScrabbleClient, my_index=0, file_name=None):
        super().__init__()
        self.client = client
        self.bag = Bag()
        self.players = [Player(self.bag, "Joueur 1"), Player(self.bag, "Joueur 2")]
        self.current_player = False
        self.tile_board = np.full((15, 15), None)
        self.is_new = np.zeros((15, 15))
        self.selected_tile = None
        self.is_first_turn = True
        self.my_player = int(my_index)
        self.ws = client
        if file_name:
            self.load_game(file_name)
        self.title("Scrabble - Partie")
        self.geometry("1200x1000")
        self.create_widgets()

    def create_widgets(self):
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
                    elif(score_multiplier[i, j] == 2): 
                         self.ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='tomato', edgecolor="white"))
                         if(i != 7 != j): self.ax.text(j + 0.5, i + 0.5, 'MOT\nCOMPTE\nDOUBLE', ha="center", va="center", fontsize=5, color="black")
                    elif(score_multiplier[i, j] == 3): 
                         self.ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='red', edgecolor="white"))
                         self.ax.text(j + 0.5, i + 0.5, 'MOT\nCOMPTE\nTRIPLE', ha="center", va="center", fontsize=5, color="black")
                    else: 
                         self.ax.add_patch(plt.Rectangle((j, i), 1, 1,facecolor='tan', edgecolor="white"))
        self.ax.plot(7.5, 7.5, '*', markersize = 22, color = 'black')

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        self.letter = self.ax.text(0.5, 0.5, '', ha="center", va="center", fontsize=14, color="black")
        self.letter_score = self.ax.text(0.35, 0.35, '', ha="center", va="center", fontsize=5, color="black")
        self.rect = plt.Rectangle((0, 0), 1, 1, facecolor = 'bisque', edgecolor = 'black')
        self.ax.add_patch(self.rect)

        for i in range(0, 15):
            for j in range(0, 15):
                if self.tile_board[i, j]:
                    self.letter.set_position((j + 0.5, i + 0.5))
                    self.letter.set_text(self.tile_board[i, j].symbol)
                    self.letter_score.set_position((j + 0.85, i+ 0.15))
                    self.letter_score.set_text(self.tile_board[i, j].score)
                    self.rect.set_xy((j, i))
                    self.ax.draw_artist(self.rect)
                    self.ax.draw_artist(self.letter_score)
                    self.ax.draw_artist(self.letter)

        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.selected = plt.Rectangle((0, 0), 1, 1, facecolor = 'none', edgecolor = 'black')
        self.ax.add_patch(self.selected)

        self.fig.canvas.mpl_connect("motion_notify_event", self.on_move)
        self.fig.canvas.mpl_connect("button_press_event", self.on_click)
        self.fig.canvas.mpl_connect("button_release_event", self.on_release)

        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)
        self.btn_pass = ctk.CTkButton(self.btn_frame, text = "Passer son tour", command=self.pass_turn)
        self.btn_pass.grid(row=0, column=0, padx=6)
        self.btn_return = ctk.CTkButton(self.btn_frame, text = "Remettre tuiles dans main", command=self.return_to_hand_update)
        self.btn_return.grid(row=0, column=1, padx=6)
        self.btn_finish = ctk.CTkButton(self.btn_frame, text = "Valider mot", command=self.finish_turn)
        self.btn_finish.grid(row=0, column=2, padx=6)

        self.score_labels = (ctk.CTkLabel(self, text = f"Score de {self.players[0].name} : {self.players[0].score}"),
                             ctk.CTkLabel(self, text = f"Score de {self.players[1].name} : {self.players[1].score}"))
        self.score_labels[self.current_player].configure(text_color = 'red')
        self.score_labels[0].place(x=10, y=10, anchor='nw')
        self.score_labels[1].place(x=10, y=40, anchor='nw')

        self.draw_board()

    def return_to_hand(self):
        for i in range(0, 15):
            for j in range(0, 15):
                if self.is_new[i, j]:
                    self.is_new[i, j] = False
                    self.players[self.current_player].hand.append(self.tile_board[i, j])
                    self.tile_board[i, j] = None

    def return_to_hand_update(self):
        self.return_to_hand()
        self.draw_board()


    def on_click(self, event):
        if self.current_player != self.my_player:
            return
        if event.inaxes:
            x = int(event.xdata)
            y = int(event.ydata)
            player = self.players[self.my_player]
            if event.ydata < 0 and 4 <= x < len(player.hand) + 4:
                self.selected_tile = player.hand[x - 4]
                player.hand.pop(x - 4)
            elif 0 <= y < 15 and 0 <= x < 15 and self.is_new[y, x]:
                self.selected_tile = self.tile_board[y, x]
                self.tile_board[y, x] = None
                self.is_new[y, x] = False
            self.draw_board(event)

    def draw_board(self, event = None):
        self.fig.canvas.restore_region(self.background)
        local_hand = self.players[self.my_player].hand
        for i, tile in enumerate(local_hand):
            x = 4 + i + int(self.selected_tile != None and event is not None and event.ydata < 0 and event.xdata < i + 4 + 0.5)
            self.letter.set_position((x + 0.5, -0.5))
            self.letter_score.set_position((x + 0.85, -0.85))
            self.rect.set_xy((x, -1))
            self.letter.set_text(tile.symbol)
            self.letter_score.set_text(tile.score)
            self.ax.draw_artist(self.rect)
            self.ax.draw_artist(self.letter_score)
            self.ax.draw_artist(self.letter)

        opp_index = 1 - self.my_player
        opp_count = len(self.players[opp_index].hand)
        self.letter.set_position((0.5, 15.2))
        self.letter.set_text(f"Adversaire : {opp_count} tuiles")
        self.ax.draw_artist(self.letter)

        for i, row in enumerate(self.tile_board):
            for j, tile in enumerate(row):
                if tile:
                    self.letter.set_position((j + 0.5, i + 0.5))
                    self.letter.set_text(tile.symbol)
                    self.letter_score.set_position((j + 0.85, i + 0.15))
                    self.letter_score.set_text(tile.score)
                    self.rect.set_xy((j, i))
                    self.ax.draw_artist(self.rect)
                    self.ax.draw_artist(self.letter_score)
                    self.ax.draw_artist(self.letter)

        if self.selected_tile and event is not None and event.inaxes:
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
        if self.current_player != self.my_player:
            if self.selected_tile:
                self.players[self.my_player].hand.append(self.selected_tile)
                self.selected_tile = None
            return

        if self.selected_tile:
            if event.inaxes:
                x = int(event.xdata)
                y = int(event.ydata)
                if 0 <= event.ydata and not self.tile_board[y, x]:
                    self.is_new[y, x] = True
                    self.tile_board[y, x] = self.selected_tile
                else:
                    player = self.players[self.my_player]
                    player.hand.insert(max(0, min( int(event.xdata - 3.5), len(player.hand))), self.selected_tile)
            else:
                self.players[self.my_player].hand.append(self.selected_tile)
            self.selected_tile = None
            self.canvas.restore_region(self.background)
            self.draw_board(event)
            self.canvas.blit(self.ax.bbox)

    def finish_turn(self):
        if self.current_player != self.my_player:
            return
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
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
            self.players[self.current_player].draw_tiles()
            self.players[self.current_player].score += score
            self.score_labels[self.current_player].configure(text = f"Score de {self.players[self.current_player].name} : {self.players[self.current_player].score}", text_color = 'black')
            self.current_player = not self.current_player
            self.score_labels[self.current_player].configure(text_color = 'red')
            self.is_first_turn = False
            if all(len(player.hand) == 0 for player in self.players):
                fin = ctk.CTkButton(self,text = f"{self.players[self.players[0].score < self.players[1].score].name} a gangier !\n les scores finaux sont : \n{self.players[0].name} : {self.players[0].score}\n{self.players[1].name} : {self.players[1].score}\n\nCliquez pour retourner a l'acceuil",fg_color="#747ACE",width = 400,height = 400,command = lambda:self.recommencer_pratique())
                fin.place(relx=0.5, rely=0.5, anchor="center")
                fin.lift()
            self.draw_board()
            if self.client:  # ← Si multijoueur actif
                move_json = self.serialize_move()  # On transforme l’état du jeu en JSON
                print("Sending move:", move_json)
                self.client.send_raw(move_json)   # ← Envoi au serveur WebSocket


    def load_move(self, data_json):  # ← Appelé quand un message arrive du serveur
        data = json.loads(data_json)

        # Met à jour l'état local selon l’action de l’adversaire
        # (scores, mains, plateau)

        data = json.loads(data_json)
        self.current_player = int(data.get('current_player', self.current_player))
        self.players[0].score, self.players[1].score = data['scores']

        for i, lbl in enumerate(self.score_labels):
            lbl.configure(
                text=f"Score de {self.players[i].name} : {self.players[i].score}",
                text_color='red' if i == self.current_player else 'black'
            )

        for i, hand_data in enumerate(data['hands']):
            self.players[i].hand = [Tile(t[0], int(t[1:])) for t in hand_data]

        for i, row in enumerate(data['board']):
            for j, cell in enumerate(row):
                self.tile_board[i, j] = Tile(cell[0], int(cell[1:])) if cell else None
                self.is_new[i, j] = False

        self.bag.tiles = [Tile(t[0], int(t[1:])) for t in data['bag']]
        self.bag.tiles_left = len(self.bag.tiles)

        self.after(0, self.draw_board)

    def serialize_move(self):#######################
        data = {
            'type': 'move',
            'room': self.client.room_id if self.client else None,
            'current_player': int(self.current_player),
            'scores': [int(p.score) for p in self.players],
            'is_first_turn': int(self.is_first_turn),
            'hands': [[f"{t.symbol}{int(t.score)}" for t in p.hand] for p in self.players],
            'board': [[f"{t.symbol}{int(t.score)}" if t else None for t in row] for row in self.tile_board],
            'bag': [f"{t.symbol}{int(t.score)}" for t in self.bag.tiles]
        }
        return json.dumps(data)
    def pass_turn(self):
        if self.current_player != self.my_player:
            return
        self.return_to_hand()
        self.players[self.current_player].redraw()

        self.score_labels[self.current_player].configure(text_color='black')
        self.current_player = not self.current_player
        self.score_labels[self.current_player].configure(text_color='red')
        self.draw_board()

        if self.client:  # ← Envoie “passer son tour” au serveur
            move_json = self.serialize_move()
            data = json.loads(move_json)
            data['action'] = 'pass'
            self.client.send_raw(json.dumps(data))


    def on_move(self, event):
        if self.selected_tile and event.inaxes:
            self.canvas.restore_region(self.background)
            self.draw_board(event)
            self.canvas.blit(self.ax.bbox)

    def calc_score(self):
        tiles_placed = self.players[self.current_player].hand_max_size - len(self.players[self.current_player].hand)
        for i in range(14, -1, -1):
            for j in range(0, 15):
                if self.is_new[i, j]:
                    total_score = 0
                    isConnected = False

                    horizontal_num = 0
                    xs = j + 1
                    while xs < 15 and self.tile_board[i, xs]:
                        horizontal_num += self.is_new[i, xs]
                        xs += 1

                    vertical_num = 0
                    ys = i - 1
                    while ys >= 0 and self.tile_board[ys, j]:
                        vertical_num += self.is_new[ys, j]
                        ys -= 1

                    if horizontal_num:
                        if horizontal_num != tiles_placed - 1: return False
                        current_score = 0
                        current_word = []
                        word_multiplier = 1
                        ys, xs = i, j
                        while xs > 0 and self.tile_board[ys, xs - 1]: xs -= 1
                        while xs < 15 and self.tile_board[ys, xs]:
                            current_word.append(self.tile_board[ys, xs].symbol)
                            if self.is_new[ys, xs]:
                                word_multiplier *= score_multiplier[ys, xs]
                                current_score += self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                if (ys < 14 and self.tile_board[ys + 1, xs]) or (ys > 0 and self.tile_board[ys - 1, xs]):
                                    isConnected = True
                                    intersecting_score = self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                    intersecting_word = [self.tile_board[ys, xs].symbol]
                                    y = ys + 1
                                    while y < 15 and self.tile_board[y, xs]:
                                        intersecting_word.append(self.tile_board[y, xs].symbol)
                                        intersecting_score += self.tile_board[y, xs].score
                                        y += 1
                                    intersecting_word = intersecting_word[::-1]
                                    y = ys - 1
                                    while y >= 0 and self.tile_board[y, xs]:
                                        intersecting_word.append(self.tile_board[y, xs].symbol)
                                        intersecting_score += self.tile_board[y, xs].score
                                        y -= 1
                                    if Dictionary().is_word_valid(tuple(intersecting_word)): total_score += intersecting_score * score_multiplier[ys, xs]
                                    else: return False
                            else:
                                isConnected = True
                                current_score += self.tile_board[ys, xs].score
                            xs += 1
                        if Dictionary().is_word_valid(tuple(current_word)): total_score += current_score * word_multiplier
                        else: return False

                    elif vertical_num:
                        if vertical_num != tiles_placed - 1: return False
                        current_score = 0
                        current_word = []
                        word_multiplier = 1
                        ys, xs = i, j
                        while ys < 14 and self.tile_board[ys + 1, xs]: ys += 1
                        while ys >= 0 and self.tile_board[ys, xs]:
                            current_word.append(self.tile_board[ys, xs].symbol)
                            if self.is_new[ys, xs]:
                                word_multiplier *= score_multiplier[ys, xs]
                                current_score += self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                if (xs < 14 and self.tile_board[ys, xs + 1]) or (xs > 0 and self.tile_board[ys, xs - 1]):
                                    isConnected = True
                                    intersecting_score = self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                                    intersecting_word = [self.tile_board[ys, xs].symbol]
                                    x = xs - 1
                                    while x >= 0 and self.tile_board[ys, x]:
                                        intersecting_word.append(self.tile_board[ys, x].symbol)
                                        intersecting_score += self.tile_board[ys, x].score
                                        x -= 1
                                    intersecting_word = intersecting_word[::-1]
                                    x = xs + 1
                                    while x < 15 and self.tile_board[ys, x]:
                                        intersecting_word.append(self.tile_board[ys, x].symbol)
                                        intersecting_score += self.tile_board[ys, x].score
                                        x += 1
                                    if Dictionary().is_word_valid(tuple(intersecting_word)): total_score += intersecting_score * score_multiplier[ys, xs]
                                    else: return False
                            else:
                                isConnected = True
                                current_score += self.tile_board[ys, xs].score
                            ys -= 1
                        if Dictionary().is_word_valid(tuple(current_word)): total_score += current_score * word_multiplier
                        else: return False
                    else:
                        if tiles_placed != 1: return False
                        ys, xs = i, j
                        if (xs < 14 and self.tile_board[ys, xs + 1]) or (xs > 0 and self.tile_board[ys, xs - 1]):
                            isConnected = True
                            intersecting_score = self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                            intersecting_word = [self.tile_board[ys, xs].symbol]
                            x = xs - 1
                            while x >= 0 and self.tile_board[ys, x]:
                                intersecting_word.append(self.tile_board[ys, x].symbol)
                                intersecting_score += self.tile_board[ys, x].score
                                x -= 1
                            intersecting_word = intersecting_word[::-1]
                            x = xs + 1
                            while x < 15 and self.tile_board[ys, x]:
                                intersecting_word.append(self.tile_board[ys, x].symbol)
                                intersecting_score += self.tile_board[ys, x].score
                                x += 1
                            if Dictionary().is_word_valid(tuple(intersecting_word)): total_score += intersecting_score * score_multiplier[ys, xs]
                            else: return False

                        if (ys < 14 and self.tile_board[ys + 1, xs]) or (ys > 0 and self.tile_board[ys - 1, xs]):
                            isConnected = True
                            intersecting_score = self.tile_board[ys, xs].score * letter_multiplier[ys, xs]
                            intersecting_word = [self.tile_board[ys, xs].symbol]
                            y = ys + 1
                            while y < 15 and self.tile_board[y, xs]:
                                intersecting_word.append(self.tile_board[y, xs].symbol)
                                intersecting_score += self.tile_board[y, xs].score
                                y += 1
                            intersecting_word = intersecting_word[::-1]
                            y = ys - 1
                            while y >= 0 and self.tile_board[y, xs]:
                                intersecting_word.append(self.tile_board[y, xs].symbol)
                                intersecting_score += self.tile_board[y, xs].score
                                y -= 1
                            if Dictionary().is_word_valid(tuple(intersecting_word)): total_score += intersecting_score * score_multiplier[ys, xs]
                            else: return False
                    if tiles_placed == 7: total_score += 50
                    if isConnected or (self.is_first_turn and self.is_new[7, 7]): return total_score
                    return False

class WelcomeWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.client = ScrabbleClient(on_message_callback=self.on_server_message)###############
        self.title("Scrabble Multijoueur 🎲 - Accueil")
        self.geometry("450x350")
        self.resizable(False, False)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title_label = ctk.CTkLabel(self, text="Rejoindre ou Créer une Partie", 
                                        font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, pady=(30, 15), padx=50, sticky="n")
        self.label = ctk.CTkLabel(self, text="Entrez un Room ID (ex: SALLE123):")
        self.label.grid(row=1, column=0, pady=(5, 0), sticky="s")
        self.entry = ctk.CTkEntry(self, width=250, placeholder_text="ROOM ID")
        self.entry.grid(row=2, column=0, pady=10, sticky="n")
        self.btn_create = ctk.CTkButton(self, text="➕ Créer une partie", 
                                        command=self.on_create, width=250, height=40)
        self.btn_create.grid(row=3, column=0, pady=5, sticky="n")
        self.btn_join = ctk.CTkButton(self, text="➡️ Rejoindre une partie", 
                                      command=self.on_join, width=250, height=40,
                                      fg_color="darkgreen", hover_color="green")
        self.btn_join.grid(row=4, column=0, pady=5, sticky="n")
        self.status = ctk.CTkLabel(self, text="Statut: Déconnecté", text_color="orange")
        self.status.grid(row=5, column=0, pady=(20, 10), sticky="s")
        self.game_window = None

    def on_server_message(self, raw_msg):  # ← raw_msg = message texte JSON reçu du serveur
        def _handle():
            try:
                data = json.loads(raw_msg)  # On convertit le texte JSON en dictionnaire Python
                t = data.get('type')        # On récupère le type d'évènement envoyé par le serveur

                # ----- Différents types de messages reçus du serveur -----

                if t == 'room_created':  
                    # Le serveur confirme que la salle a été créée
                    print(f"Salle {data.get('room')} créée")

                elif t == 'join_success':
                    # Le serveur confirme que le joueur a bien rejoint la salle
                    print("Rejoint avec succès")

                elif t == 'opponent_joined':
                    # L'adversaire vient d'arriver dans la salle
                    # Si la fenêtre de jeu est ouverte, on met à jour le titre
                    if self.game_window:
                        self.game_window.title(f"Scrabble - Partie dans {self.client.room_id}")

                elif t == 'move':
                    # Le serveur envoie un coup joué par l'adversaire
                    if self.game_window:
                        self.game_window.load_move(raw_msg)  # On laisse GameWindow appliquer le coup

                else:
                    # Si le type n'existe pas, on affiche l'objet entier
                    print(str(data))

            except Exception as e:
                print('Error handling server message:', e)

        # On exécute le traitement dans le thread Tkinter
        self.after(0, _handle)


    def on_create(self):
        room = self.entry.get().strip().upper()  # On récupère le nom de salle entré par l'utilisateur

        if not room:
            # Aucun texte → erreur utilisateur
            self.status.configure(text='Statut: Entrez un Room ID', text_color="red")
            return

        self.status.configure(text='Statut: Tentative de création...', text_color="grey")

        # Envoie une requête "create_room" au serveur via ScrabbleClient
        fut = self.client.create_room(room)

        try:
            # On attend la réponse du serveur (max 5 secondes)
            resp = fut.result(timeout=5)

            my_index = 0  # Le créateur de salle est toujours le joueur 0 (joueur qui commence en premier)
            self.open_game_window(my_index)  # On ouvre la fenêtre de jeu

        except Exception as e:
            # En cas d’erreur (salle déjà prise, serveur hors-ligne, etc.)
            self.status.configure(text=f"Statut: Erreur lors de la création: {e}", text_color="red")


    def on_join(self):
        room = self.entry.get().strip().upper()  # On récupère le nom de salle entré

        if not room:
            self.status.configure(text='Statut: Entrez un Room ID', text_color="red")
            return

        self.status.configure(text='Statut: Tentative de rejoindre...', text_color="grey")

        # Envoie une requête "join_room" au serveur
        fut = self.client.join_room(room)

        try:
            # Attend la réponse serveur
            resp = fut.result(timeout=5)

            # Le serveur dit que la salle n'existe pas ou est pleine
            if resp.get('type') == 'join_failed':
                self.status.configure(
                    text='Statut: Échec du join. Salle inexistante ou pleine.',
                    text_color="red"
                )
                return

            my_index = 1  # Le joueur qui rejoint est toujours le joueur 1
            self.open_game_window(my_index)  # On ouvre la fenêtre de jeu

        except Exception as e:
            # Si le serveur ne répond pas ou bug
            self.status.configure(text=f"Statut: Erreur lors du join: {e}", text_color="red")

            
    def open_game_window(self, my_index=0):
        self.withdraw()
        self.game_window = GameWindow(self.client, my_index)
        self.game_window.mainloop()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = WelcomeWindow()
    app.mainloop()
