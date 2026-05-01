import asyncio
import websockets

PORT = 8080

players = set()

async def handler(websocket):
    players.add(websocket)
    addr = websocket.remote_address
    print(f'New connection from {addr}')

    try:
        # create connection
        async for message in websocket:
            print(f"Received: {message} from {addr}")

            if message == 'InsertLine':
                # relay to other players
                for player in players:
                    if player != websocket:
                        await player.send('InsertLine')

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        # cleanup
        print(f'Disconnecting {addr}')
        players.remove(websocket)

async def main(address, port):
    async with websockets.serve(handler, address, port):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main('0.0.0.0', PORT))
