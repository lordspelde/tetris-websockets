import tetris
import threading
import websockets
import asyncio

ADDR = 'localhost' # set to server IP
PORT = 8080

run, blocks = tetris.load()

current_websocket = None

# asyncio thread loop required to share websocket
thread_loop = asyncio.new_event_loop()
asyncio.set_event_loop(thread_loop)

async def main():
    global current_websocket
    url = f'ws://{ADDR}:{PORT}'

    # connect to server
    async with websockets.connect(url) as websocket:
        print(f'Connected to {url}')

        # update websocket so line completion can send to the server
        current_websocket = websocket

        # listen for incoming messages
        async for message in websocket:
            print(f'Received: {message}')
            if message == 'InsertLine':
                blocks.insert_row()

def on_line_completion(enemy_line_cleared):
    if enemy_line_cleared:
        # "enemy lines" should not count
        print('Enemy line cleared')
        return
    
    print('Line completed!')
    
    # tell server a line has been cleared
    asyncio.run_coroutine_threadsafe(current_websocket.send('InsertLine'), thread_loop)

# link callback for cleared lines
blocks.line_completion_callback = on_line_completion

def start():
    asyncio.set_event_loop(thread_loop)
    thread_loop.run_until_complete(main())

# run networked component
t = threading.Thread(target=start)
t.start()

# main game loop
run()