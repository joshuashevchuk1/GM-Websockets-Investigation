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

        loop = asyncio.get_running_loop()

        def callback(indata, frames, time, status):
            # Convert audio and schedule sending in the main thread-safe way
            loop.call_soon_threadsafe(
                asyncio.create_task,
                websocket.send(indata.tobytes())
            )

        # Start audio stream from mic
        with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype='int16',
                            blocksize=CHUNK_SIZE, callback=callback):
            print("Recording and sending... (Ctrl+C to stop)")

            while True:
                # Wait to receive echoed audio
                echoed_data = await websocket.recv()
                audio_np = np.frombuffer(echoed_data, dtype='int16')
                sd.play(audio_np, samplerate=RATE)
                await asyncio.sleep(CHUNK_DURATION)

asyncio.run(record_and_stream())
