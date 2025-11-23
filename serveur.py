import asyncio
import websockets
import json

rooms = {}  # {"ROOM_ID": {"players": [ws1, ws2], "gameState": ... }}

# ---------------------- HANDLER ----------------------
async def handler(ws):
    async for msg in ws:
        try:
            data = json.loads(msg)
        except Exception:
            continue  # ignore les messages invalides

        if data["type"] == "create_room":
            room_id = data["room"]
            rooms[room_id] = {"players": [ws]}
            await ws.send(json.dumps({"type": "room_created", "room": room_id}))

        elif data["type"] == "join_room":
            room_id = data["room"]
            if room_id in rooms and len(rooms[room_id]["players"]) < 2:
                rooms[room_id]["players"].append(ws)
                await ws.send(json.dumps({"type": "join_success"}))

                # Notifier l’autre joueur
                for p in rooms[room_id]["players"]:
                    if p != ws:
                        await p.send(json.dumps({"type": "opponent_joined"}))
            else:
                await ws.send(json.dumps({"type": "join_failed"}))

        elif data["type"] == "move":
            room_id = data["room"]
            if room_id in rooms:
                for p in rooms[room_id]["players"]:
                    if p != ws:
                        await p.send(json.dumps(data))

# ---------------------- SERVEUR ----------------------
async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("🚀 Serveur Scrabble démarré sur le port 8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())