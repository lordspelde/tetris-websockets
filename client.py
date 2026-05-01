import tetris
import threading
import websockets
import asyncio

ADDR = 'localhost'
PORT = 8080

run, blocks = tetris.load()

current_websocket = None

thread_loop = asyncio.new_event_loop()
asyncio.set_event_loop(thread_loop)

async def main():
    global current_websocket
    url = f'ws://{ADDR}:{PORT}'

    async with websockets.connect(url) as websocket:
        print(f'Connected to {url}')

        current_websocket = websocket

        async for message in websocket:
            print(f'Received: {message}')
            if message == 'InsertLine':
                blocks.insert_row()

def on_line_completion():
    print('Line completed!')
    asyncio.run_coroutine_threadsafe(current_websocket.send('InsertLine'), thread_loop)

blocks.line_completion_callback = on_line_completion

def start():
    asyncio.set_event_loop(thread_loop)
    thread_loop.run_until_complete(main())

t = threading.Thread(target=start)
t.start()

run()