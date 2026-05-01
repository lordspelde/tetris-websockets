# Tetris WebSockets

Implementation of Tetris Battle using Python's websocket module

Original game can be found [here](https://pythonassets.com/posts/tetris-with-pygame/)

## Getting Started

- Note: Make sure you are on Python 3.13 or older, the latest version of Python 3.14 does not have a pygame release yet

Make sure your `pip` is up to date

```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

Install required dependencies

- `pip install -r requirements.txt`

## Running the Code

If wanting to play single-player, you can directly run the `tetris.py` file.

Otherwise, run `server.py` and `client.py` separately, updating the `ADDR` variable as necessary to connect to other computers.

## Controls

- Left & Right Arrow keys to move side to side
- Up Arrow Key to rotate
- Down Arrow Key to drop
- G: Insert a "junk row" that would otherwise only appear in multiplayer