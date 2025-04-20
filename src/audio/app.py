import asyncio
import websockets

async def handle_audio(websocket):
    print("Client connected.")
    try:
        while True:
            audio_data = await websocket.recv()  # Receive the audio batch
            print(f"Received batch of {len(audio_data)} bytes")

            # Echo it back
            await websocket.send(audio_data)
            print("Echoed batch back.")
    except websockets.ConnectionClosed:
        print("Client disconnected.")

async def main():
    async with websockets.serve(handle_audio, "localhost", 8765, ping_interval=30, ping_timeout=20):
        print("Server started at ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
