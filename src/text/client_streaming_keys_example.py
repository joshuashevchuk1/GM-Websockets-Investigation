import asyncio
import websockets
from aioconsole import ainput

async def send_messages(websocket):
    while True:
        message = await ainput("You: ")  # non-blocking input
        # Send in chunks if you want to simulate partials
        for i in range(1, len(message) + 1):
            await websocket.send(f"[PARTIAL]: {message[:i]}")
            await asyncio.sleep(0.05)  # simulate typing delay
        await websocket.send(f"[FINAL]: {message}")

async def receive_messages(websocket):
    async for response in websocket:
        print(f"\n< Server: {response}")

async def client():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        await asyncio.gather(send_messages(websocket), receive_messages(websocket))

if __name__ == "__main__":
    asyncio.run(client())
