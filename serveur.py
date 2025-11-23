import asyncio
import websockets
import json

players = []   # [ws1, ws2]

async def handler(ws):
    global players

    # Trop de joueurs ?
    if len(players) >= 2:
        await ws.send(json.dumps({"type": "server_full"}))
        await ws.close()
        return

    # Ajouter le joueur
    players.append(ws)
    player_id = len(players)
    print(f"🟢 Joueur {player_id} connecté")

    await ws.send(json.dumps({"type": "connected", "player": player_id}))

    # Si 2 joueurs → la partie est prête
    if len(players) == 2:
        print("🎮 Les deux joueurs sont connectés, partie prête !")
        for p in players:
            await p.send(json.dumps({"type": "ready"}))

    try:
        async for msg in ws:
            data = json.loads(msg)

            if data["type"] == "move":
                # envoyer le move à l’autre joueur
                for p in players:
                    if p != ws:
                        await p.send(json.dumps(data))

    except websockets.ConnectionClosed:
        pass

    # Déconnexion du joueur
    print(f"🔴 Joueur {player_id} déconnecté")
    players.remove(ws)

    # Dire à l’autre joueur qu’il reste seul
    for p in players:
        await p.send(json.dumps({"type": "opponent_left"}))


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("🚀 Serveur Scrabble démarré sur le port 8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
