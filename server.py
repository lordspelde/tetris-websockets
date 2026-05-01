import socket
import threading
import asyncio
import websockets

PORT = 8080

players = {}

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', PORT))
s.listen()

print(f'Web server listening on {PORT}')

def handle_client(connection, address):
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break

            data = data.decode()
            print(f"Received: {data}")

            if data == 'InsertLine':
                for addr, player in players.items():
                    if addr != address:
                        player['connection'].sendall('InsertLine'.encode())

    finally:
        print(f'Disconnecting {address}')
        connection.close()
        del players[address]


while True:
    try:
        connection, address = s.accept()
        print(f'New connection from {address}')

        t = threading.Thread(target=handle_client, args=(connection, address))
        t.start()

        players[address] = {
            'connection': connection,
            'thread': t,
        }

    except KeyboardInterrupt:
        print('Stopping')
        break

s.close()

for addr, player in players.items():
    player['connection'].close()
    player['thread'].join()