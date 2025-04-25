import asyncio
import websockets
import numpy as np
import sounddevice as sd

# Audio settings — adjust if your audio format differs
SAMPLE_RATE = 16000  # Hz
CHANNELS = 1
DTYPE = 'int16'

async def playback(message):
    await asyncio.sleep(1)  # 1 second delay before playback

    # Convert raw bytes to numpy array
    audio_array = np.frombuffer(message, dtype=DTYPE)

    # Playback audio using sounddevice
    print(f"[Playback] Playing audio ({len(audio_array)} samples)...")
    sd.play(audio_array, samplerate=SAMPLE_RATE)
    sd.wait()  # Wait for playback to finish

async def handle_audio(websocket):
    print("Client connected.")
    try:
        async for message in websocket:
            print(f"Received batch of {len(message)} bytes")

            # Start the playback task asynchronously
            asyncio.create_task(playback(message))

    except websockets.ConnectionClosed:
        print("Client disconnected.")

async def main():
    async with websockets.serve(handle_audio, "localhost", 8765):
        print("Server started at ws://localhost:8765")
        await asyncio.Future()  # Run forever

asyncio.run(main())
