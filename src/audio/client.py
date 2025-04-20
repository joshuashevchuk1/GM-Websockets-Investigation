import asyncio
import websockets
import sounddevice as sd
import numpy as np

RATE = 16000
CHUNK_DURATION = 5  # seconds
CHUNK_SIZE = int(RATE * CHUNK_DURATION)
CHANNELS = 1

# TODO: fix audio repeat loops
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
                print(f"Received echoed data of size {len(echoed_data)} bytes")

                # Convert the received audio data back into a numpy array for playback
                audio_np = np.frombuffer(echoed_data, dtype='int16')

                # Play the audio back
                sd.play(audio_np, samplerate=RATE)
                print("Playing echoed audio...")

                # Wait for the audio to finish playing before processing the next chunk
                await asyncio.sleep(CHUNK_DURATION)

                # After playing the chunk, clear the buffer to avoid repeating audio
                # This ensures the next chunk is independent
                # (No further action needed, as we directly process the new chunk)

                # Give time to other tasks (non-blocking)
                await asyncio.sleep(0.1)

asyncio.run(record_and_stream())
