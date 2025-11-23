import asyncio
import websockets
import json

# Une seule partie, jusqu'à 2 joueurs
players = []

async def handler(ws):
    global players
    players.append(ws)
    print(f"Nouvel joueur connecté ({len(players)}/2)")

    if len(players) == 2:
        # Notifier les deux joueurs que la partie peut commencer
        for p in players:
            await p.send(json.dumps({"type": "start_game"}))

    try:
        async for msg in ws:
            data = json.loads(msg)
            if data["type"] == "move":
                # transmettre le move à l'autre joueur
                for p in players:
                    if p != ws:
                        await p.send(msg)
    except Exception as e:
        print("Erreur websocket:", e)
    finally:
        print("Joueur déconnecté")
        players.remove(ws)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("🚀 Serveur Scrabble démarré sur le port 8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
