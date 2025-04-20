import asyncio
import websockets

async def send_messages(websocket):
    while True:
        msg = input("You: ")
        await websocket.send(msg)
        print(f"> Sent: {msg}")

async def receive_messages(websocket):
    while True:
        response = await websocket.recv()
        print(f"< Received: {response}")

async def client():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        # Run both send and receive tasks concurrently
        send_task = asyncio.create_task(send_messages(websocket))
        receive_task = asyncio.create_task(receive_messages(websocket))
        await asyncio.gather(send_task, receive_task)

if __name__ == "__main__":
    asyncio.run(client())
