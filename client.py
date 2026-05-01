import socket
import tetris
import threading

ADDR = '100.98.54.78'
PORT = 8080

s = socket.socket()
s.connect((ADDR, PORT))

print(f'Connected to {ADDR}:{PORT}')

running = True
run, blocks = tetris.load()

def on_line_completion():
    print('Line completed!')
    s.sendall('InsertLine'.encode())

def recv():
    while running:
        try:
            data = s.recv(1024)
            if not data:
                break

            data = data.decode()
            print(f"Received: {data}")

            if data == 'InsertLine':
                blocks.insert_row()

        except Exception as e:
            print(f"Error receiving data: {e}")
            break

blocks.line_completion_callback = on_line_completion

t = threading.Thread(target=recv)
t.start()

run()

running = False

s.close()
t.join()