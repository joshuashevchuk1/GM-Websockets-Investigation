import asyncio
import websockets


async def client():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")
        await websocket.send(name)
        print(f"> Sent: {name}")

        response = await websocket.recv()
        print(f"< Received: {response}")


if __name__ == "__main__":
    asyncio.run(client())