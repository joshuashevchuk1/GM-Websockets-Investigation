import asyncio
import websockets
import sounddevice as sd
import numpy as np

RATE = 16000
CHUNK_DURATION = 5  # seconds
CHUNK_SIZE = int(RATE * CHUNK_DURATION)
CHANNELS = 1

async def record_and_stream():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Connected to server")

        while True:
            # Record a 5-second chunk of audio-batch
            print("Recording 5-second chunk...")
            audio_chunk = sd.rec(CHUNK_SIZE, samplerate=RATE, channels=CHANNELS, dtype='int16')
            sd.wait()  # Wait until recording is done

            # Send the recorded audio-batch
            await websocket.send(audio_chunk.tobytes())
            print("Sent chunk to server, waiting for echo...")

            # Wait for echoed data
            echoed_data = await websocket.recv()
            print(f"Received echoed chunk ({len(echoed_data)} bytes)")

            # Play the echoed audio-batch
            audio_np = np.frombuffer(echoed_data, dtype='int16')
            sd.play(audio_np, samplerate=RATE)
            sd.wait()

asyncio.run(record_and_stream())
