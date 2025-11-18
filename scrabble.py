# ------------------------------
# Scrabble Multiplayer Client (with Lobby + Welcome Window + Game Window)
# Integrated with your existing Scrabble logic.
# ------------------------------
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

# ------------------------------
# CONFIG
# ------------------------------
SERVER_IP = "ws://143.198.52.17:8765"   # <-- replace with your server IP if different

# ------------------------------
# WebSocket client helper that runs its own event loop in a thread

# ------------------------------
 # ---------------- Multiplicateurs ----------------
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
        # ---------------------------------------------------
import asyncio
import websockets
import threading
import json

SERVER_IP = "ws://165.227.38.141:8765"


class ScrabbleClient:
    def __init__(self, on_message_callback=None):
        self.ws = None
        self.room_id = None
        self.on_message = on_message_callback

        # event loop dédié dans un thread séparé (non bloquant pour Tkinter)
        self.loop = asyncio.new_event_loop()

        def _start_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        t = threading.Thread(target=_start_loop, args=(self.loop,), daemon=True)
        t.start()

    def _run(self, coro):
        """Exécute une coroutine asyncio dans le thread dédié."""
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    # --------------------------------------------------------
    #  CONNEXION AU SERVEUR (INCLUANT TEST)
    # --------------------------------------------------------
    async def _connect(self):
        try:
            print("Connexion au serveur…")
            self.ws = await websockets.connect(SERVER_IP)
            print("Connexion réussie.")
        except Exception as e:
            print("❌ Impossible de se connecter au serveur :", e)
            self.ws = None
            raise

    def connect(self):
        """Appelé depuis Tkinter / synchronisé."""
        future = self._run(self._connect())
        return future

    # --------------------------------------------------------
    #  CRÉATION DE SALLE
    # --------------------------------------------------------
    async def _create_room(self, room):
        self.room_id = room

        if self.ws is None:
            await self._connect()

        if self.ws is None:
            return {"status": "error", "msg": "Pas connecté au serveur."}

        await self.ws.send(json.dumps({"type": "create_room", "room": room}))
        resp = json.loads(await self.ws.recv())

        self._run(self._listen_forever())
        return resp

    def create_room(self, room):
        return self._run(self._create_room(room))

    # --------------------------------------------------------
    #  REJOINDRE UNE SALLE
    # --------------------------------------------------------
    async def _join_room(self, room):
        self.room_id = room

        if self.ws is None:
            await self._connect()

        if self.ws is None:
            return {"status": "error", "msg": "Pas connecté au serveur."}

        await self.ws.send(json.dumps({"type": "join_room", "room": room}))
        resp = json.loads(await self.ws.recv())

        self._run(self._listen_forever())
        return resp

    def join_room(self, room):
        return self._run(self._join_room(room))

    # --------------------------------------------------------
    #  ÉCOUTE PERMANENTE DES MESSAGES DU SERVEUR
    # --------------------------------------------------------
    async def _listen_forever(self):
        while True:
            try:
                msg = await self.ws.recv()
                data = json.loads(msg)

                if self.on_message:
                    self.on_message(self, data)

            except Exception:
                print("❌ Perte de connexion avec le serveur.")
                break


    def join_room(self, room):
        return self._run(self._join_room(room))

    async def _listen_forever(self):
        try:
            async for msg in self.ws:
                # forward raw message to callback on main thread
                if self.on_message:
                    # call callback in main thread via tkinter "after"
                    try:
                        data = msg
                        self.on_message(data)
                    except Exception as e:
                        print("Error handling incoming message:", e)
        except Exception as e:
            print("WebSocket listen stopped:", e)

    def send_json(self, obj):
        # schedule send on the client's loop
        if self.ws is None:
            print("WebSocket not connected yet")
            return
        return self._run(self.ws.send(json.dumps(obj)))

    def send_raw(self, raw_json):
        if self.ws is None:
            print("WebSocket not connected yet")
            return
        return self._run(self.ws.send(raw_json))

# ------------------------------
# Game Window (wrap your Scrabble UI into a class that accepts a client)
# ------------------------------
class GameWindow(ctk.CTkToplevel):
    def __init__(self, client: ScrabbleClient, file_name=None,parent = None):
        super().__init__()
        self.client = client
        self.parent = parent
        # create the Scrabble state (adapted from your pasted code)
        self.bag = Bag()
        self.players = [Player(self.bag, "Joueur 1"), Player(self.bag, "Joueur 2")]
        self.current_player = False
        self.tile_board = np.full((15, 15), None)
        self.is_new = np.zeros((15, 15))
        self.selected_tile = None
        self.is_first_turn = True
        self.ws = client
        if file_name:
            self.load_game(file_name)
        self.title("Scrabble - Partie")
        self.geometry("900x900")
        self.focus_set()      # met le focus sur cette fenêtre
        self.transient(self.parent)  # lève la fenêtre au-dessus du parent
        self.create_widgets()

    def create_widgets(self):
        # draw board
        self.fig, self.ax = plt.subplots(figsize=(9, 9))
        self.ax.set_aspect("equal")
        self.ax.set_xlim(0, 15)
        self.ax.set_ylim(-1, 15)
        self.ax.axis("off")
        # board squares
        for i in range(15):
            for j in range(15):
                if(letter_multiplier[i, j] == 2):
                    self.ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='lightskyblue', edgecolor="white"))
                elif(letter_multiplier[i, j] == 3):
                    self.ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='dodgerblue', edgecolor="white"))
                elif(score_multiplier[i, j] == 2):
                    self.ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='tomato', edgecolor="white"))
                elif(score_multiplier[i, j] == 3):
                    self.ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='red', edgecolor="white"))
                else:
                    self.ax.add_patch(plt.Rectangle((j, i), 1, 1, facecolor='tan', edgecolor="white"))
        self.ax.plot(7.5, 7.5, '*', markersize = 22, color = 'black')

        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # reusable text artists
        self.letter = self.ax.text(0.5, 0.5, '', ha="center", va="center", fontsize=14, color="black")
        self.letter_score = self.ax.text(0.35, 0.35, '', ha="center", va="center", fontsize=5, color="black")
        self.rect = plt.Rectangle((0, 0), 1, 1, facecolor = 'bisque', edgecolor = 'black')
        self.ax.add_patch(self.rect)

        # draw existing tile_board
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

        # control buttons
        self.btn_frame = ctk.CTkFrame(self)
        self.btn_frame.pack(pady=10)
        self.btn_pass = ctk.CTkButton(self.btn_frame, text = "Passer son tour", command=self.skip)
        self.btn_pass.grid(row=0, column=0, padx=6)
        self.btn_return = ctk.CTkButton(self.btn_frame, text = "Remettre tuiles dans main", command=self.return_to_hand_update)
        self.btn_return.grid(row=0, column=1, padx=6)
        self.btn_finish = ctk.CTkButton(self.btn_frame, text = "Valider mot", command=self.finish_turn)
        self.btn_finish.grid(row=0, column=2, padx=6)

        # score labels
        self.score_labels = (ctk.CTkLabel(self, text = f"Score de {self.players[0].name} : {self.players[0].score}"),
                             ctk.CTkLabel(self, text = f"Score de {self.players[1].name} : {self.players[1].score}"))
        self.score_labels[self.current_player].configure(text_color = 'red')
        self.score_labels[0].pack(anchor='nw')
        self.score_labels[1].pack(anchor='nw')

        self.draw_board()

    # --- many methods copied/adapted from your original code ---
    def load_game(self, file_name):
        try:
            with open(file_name, 'r') as file:
                self.bag.tiles = []
                self.players[0].hand = []
                self.players[1].hand = []
                lines = [line for line in file]
                self.current_player = int(lines[0].strip())
                self.players[0].score = int(lines[1].strip())
                self.players[1].score = int(lines[2].strip())
                self.is_first_turn = int(lines[3].strip())
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
                        index += 1
                for i in range(index, len(lines)):
                    l = lines[i].strip()
                    self.bag.tiles.append(Tile(l[0], int(l[1:])))
                self.bag.tiles_left = len(self.bag.tiles)
        except FileNotFoundError:
            print("Le fichier 'series.txt' n'a pas été trouvé.")
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier: {e}")

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

    def skip(self):
        self.return_to_hand()
        self.players[self.current_player].redraw()
        self.score_labels[self.current_player].configure(text_color = 'black')
        self.current_player = not self.current_player
        self.score_labels[self.current_player].configure(text_color = 'red')
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
        # draw hand
        for i, tile in enumerate(self.players[self.current_player].hand):
            x = 4 + i + int(self.selected_tile != None and event is not None and event.ydata < 0 and event.xdata < i + 4 + 0.5)
            self.letter.set_position((x + 0.5, -0.5))
            self.letter_score.set_position((x + 0.85, -0.85))
            self.rect.set_xy((x, -1))
            self.letter.set_text(tile.symbol)
            self.letter_score.set_text(tile.score)
            self.ax.draw_artist(self.rect)
            self.ax.draw_artist(self.letter_score)
            self.ax.draw_artist(self.letter)
        # draw board new tiles
        for i, row in enumerate(self.tile_board):
            for j, tile in enumerate(row):
                if(tile is not None and self.is_new[i, j]):
                    self.letter.set_position((j + 0.5, i + 0.5))
                    self.letter.set_text(tile.symbol)
                    self.letter_score.set_position((j + 0.85, i+ 0.15))
                    self.letter_score.set_text(tile.score)
                    self.rect.set_xy((j, i))
                    self.ax.draw_artist(self.rect)
                    self.ax.draw_artist(self.letter_score)
                    self.ax.draw_artist(self.letter)
        # draw dragged tile
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
        if self.selected_tile:
            if event.inaxes:
                x = int(event.xdata)
                y = int(event.ydata)
                if 0 <= event.ydata and not self.tile_board[y, x]:
                    self.is_new[y, x] = True
                    self.tile_board[y, x] = self.selected_tile
                else:
                    self.players[self.current_player].hand.insert(max(0, min( int(event.xdata - 3.5), len(self.players[self.current_player].hand))), self.selected_tile)
            else:
                self.players[self.current_player].hand.append(self.selected_tile)
            self.selected_tile = None
            self.canvas.restore_region(self.background)
            self.draw_board(event)
            self.canvas.blit(self.ax.bbox)

    def finish_turn(self):
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
            # send move to server (serialize state)
            if self.client:
                move_json = self.serialize_move()
                print("Sending move:", move_json)
                self.client.send_raw(move_json)

    def save_game(self, file_name):
        self.return_to_hand()
        with open(file_name, 'w') as file:
            file.write(f"{int(self.current_player)}\n")
            file.write(f"{self.players[0].score}\n")
            file.write(f"{self.players[1].score}\n")
            file.write(f"{int(self.is_first_turn)}\n")
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

    def load_move(self, data_json):
        data = json.loads(data_json)
        self.current_player = data['current_player']
        self.players[0].score, self.players[1].score = data['scores']
        self.is_first_turn = bool(data['is_first_turn'])
        # Recréer les mains
        for i, hand_data in enumerate(data['hands']):
            self.players[i].hand = [Tile(t[0], int(t[1:])) for t in hand_data]
        # Recréer le plateau
        for i, row in enumerate(data['board']):
            for j, cell in enumerate(row):
                self.tile_board[i, j] = Tile(cell[0], int(cell[1:])) if cell else None
        # Recréer le sac
        self.bag.tiles = [Tile(t[0], int(t[1:])) for t in data['bag']]
        self.bag.tiles_left = len(self.bag.tiles)
        # redraw on main thread safely
        self.after(0, self.draw_board)

    def serialize_move(self):
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

    # simplified / unchanged scoring routine
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

# ------------------------------
# Welcome Window (creates or joins a room and opens GameWindow)
# ------------------------------
class WelcomeWindow(ctk.CTkToplevel):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent   # <-- on enregistre le parent
        self.client = ScrabbleClient(on_message_callback=self.on_server_message)

        self.title("Scrabble Multiplayer - Accueil")
        self.geometry("400x200")

        self.label = ctk.CTkLabel(self, text="Room ID:")
        self.label.pack(pady=10)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=5)


        self.btn_create = ctk.CTkButton(self, text="Créer une partie", command=self.on_create)
        self.btn_create.pack(pady=6)

        self.btn_join = ctk.CTkButton(self, text="Rejoindre une partie", command=self.on_join)
        self.btn_join.pack(pady=6)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack(pady=6)

        self.focus_set()      # met le focus sur cette fenêtre
        self.transient(parent)  # lève la fenêtre au-dessus du parent

        self.game_window = None


    def on_server_message(self, raw_msg):
        # called from client's background thread; schedule to main thread
        def _handle():
            try:
                data = json.loads(raw_msg)
                t = data.get('type')
                if t == 'room_created':
                    self.status.configure(text=f"Salle {data.get('room')} créée")
                elif t == 'join_success':
                    self.status.configure(text="Rejoint avec succès")
                elif t == 'opponent_joined':
                    self.status.configure(text="Adversaire connecté — la partie peut commencer")
                elif t == 'move':
                    # forward move to game window
                    if self.game_window:
                        self.game_window.load_move(raw_msg)
                else:
                    self.status.configure(text=str(data))
            except Exception as e:
                print('Error handling server message:', e)
        self.after(0, _handle)

    def on_create(self):
        room = self.entry.get().strip().upper()
        if not room:
            self.status.configure(text='Entrez un Room ID')
            return
        fut = self.client.create_room(room)
        try:
            resp = fut.result(timeout=5)
            self.status.configure(text='Salle créée')
            # open game window
            self.open_game_window()
            # start listening
            self.client._run(self.client._listen_forever())
        except Exception as e:
            self.status.configure(text=f'Erreur create: {e}')

    def on_join(self):
        room = self.entry.get().strip().upper()
        if not room:
            self.status.configure(text='Entrez un Room ID')
            return
        fut = self.client.join_room(room)
        try:
            resp = fut.result(timeout=5)
            if resp.get('type') == 'join_failed':
                self.status.configure(text='Échec du join')
                return
            self.status.configure(text='Rejoint')
            self.open_game_window()
            # listening already started inside join_room
        except Exception as e:
            self.status.configure(text=f'Erreur join: {e}')

    def open_game_window(self):
        self.withdraw()
        self.game_window = GameWindow(self.client,self.parent)



