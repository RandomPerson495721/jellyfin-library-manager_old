from flask import Flask , render_template_string
from flask_socketio import SocketIO
import asyncio
import websockets


async def handler(websocket):
    while True:
        message = await websocket.recv()
        print(message)
        await websocket.send(message)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())