import socket
import tetris
import threading
import websockets
import asyncio

ADDR = '100.98.54.78'
PORT = 8080

running = True
run, blocks = tetris.load()

async def main():
    url = f'ws://{ADDR}:{PORT}'

    async with websockets.connect(url) as websocket:
        print(f'Connected to {url}')

        def on_line_completion():
            print('Line completed!')
            websocket.send('InsertLine')

        blocks.line_completion_callback = on_line_completion

        while True:
            data = await websocket.recv()
            print(f'Received: {data}')

            if data == 'InsertLine':
                blocks.insert_row()

asyncio.run(main())

run()
running = False