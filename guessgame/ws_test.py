import asyncio
import websockets

async def test():
    uri = "ws://localhost:8000/ws/guessgame/"
    async with websockets.connect(uri) as websocket:
        msg = await websocket.recv()
        print("Received:", msg)

asyncio.run(test())