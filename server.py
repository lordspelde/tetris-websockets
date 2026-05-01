import socket
import threading
import asyncio
import websockets

players = set()

async def handler(websocket):
    players.add(websocket)
    addr = websocket.remote_address
    print(f'New connection from {addr}')

    try:
        while True:
            data = await websocket.recv()
            if not data:
                break

            data = data.decode()
            print(f"Received: {data}")

            if data == 'InsertLine':
                for player in players:
                    if player != websocket:
                        await player.send('InsertLine')

    finally:
        print(f'Disconnecting {addr}')
        players.remove(websocket)

async def main(address, port):
    async with websockets.serve(handler, address, port):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main('0.0.0.0', 8080))
