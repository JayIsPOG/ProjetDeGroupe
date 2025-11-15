
import asyncio
import websockets

clients = set()

async def handler(ws):
    clients.add(ws)
    try:
        async for message in ws:
            # renvoie le message à tous les clients sauf l'envoyeur
            for client in clients:
                if client != ws:
                    await client.send(message)
    finally:
        clients.remove(ws)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Serveur WebSocket en écoute sur ws://localhost:8765")
        await asyncio.Future()  # run forever

asyncio.run(main())
