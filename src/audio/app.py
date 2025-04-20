import asyncio
import websockets


async def handle_audio(websocket):
    print("Client connected.")
    try:
        async for message in websocket:
            print(f"Received batch of {len(message)} bytes")

            # Wait 5 seconds before sending it back
            #await asyncio.sleep(5)

            # Send the same chunk back
            await websocket.send(message)
            print("Echoed batch back after 5-second delay.")
    except websockets.ConnectionClosed:
        print("Client disconnected.")


async def main():
    async with websockets.serve(handle_audio, "localhost", 8765):
        print("Server started at ws://localhost:8765")
        await asyncio.Future()  # Run forever


asyncio.run(main())
