import asyncio
import websockets
import json

# ----------------------
# Partie unique
# ----------------------
players = []  # liste des websockets connectés
game_state = {}  # on pourra stocker éventuellement l'état complet

async def handler(ws):
    global players
    players.append(ws)
    try:
        # prévenons si l'autre joueur est déjà là
        if len(players) == 2:
            await asyncio.gather(*[p.send(json.dumps({"type": "opponent_joined"})) for p in players])

        async for msg in ws:
            data = json.loads(msg)
            if data["type"] in ["create_room", "join_room"]:
                await ws.send(json.dumps({"type": "join_success"}))
                # si 2 joueurs connectés, on peut commencer la partie
                if len(players) == 2:
                    for p in players:
                        await p.send(json.dumps({"type": "opponent_joined"}))
            elif data["type"] == "move":
                # renvoyer le move à l'autre joueur
                for p in players:
                    if p != ws:
                        await p.send(json.dumps(data))
    except websockets.ConnectionClosed:
        print("Un joueur s'est déconnecté")
    finally:
        if ws in players:
            players.remove(ws)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Serveur WebSocket lancé sur le port 8765")
        await asyncio.Future()  # run forever

asyncio.run(main())
