import asyncio
import websockets
import numpy as np
import sounddevice as sd

# Audio settings — adjust if your audio format differs
SAMPLE_RATE = 16000  # Hz
CHANNELS = 1
DTYPE = 'int16'
BUFFER_SIZE = SAMPLE_RATE * 1  # 1 second of audio, you can adjust the size

audio_buffer = []

async def playback():
    # Combine all accumulated audio chunks
    audio_array = np.concatenate(audio_buffer)

    # Playback audio using sounddevice
    print(f"[Playback] Playing audio ({len(audio_array)} samples)...")
    sd.play(audio_array, samplerate=SAMPLE_RATE)
    sd.wait()  # Wait for playback to finish

    # Clear the buffer after playback
    audio_buffer.clear()

async def handle_audio(websocket):
    print("Client connected.")
    try:
        async for message in websocket:
            print(f"Received batch of {len(message)} bytes")

            # Convert raw bytes to numpy array and append to buffer
            audio_array = np.frombuffer(message, dtype=DTYPE)
            audio_buffer.append(audio_array)

            # Check if buffer has enough data to start playback (e.g., after 1 second of audio)
            if len(np.concatenate(audio_buffer)) >= BUFFER_SIZE:
                # Start playback task asynchronously
                asyncio.create_task(playback())

    except websockets.ConnectionClosed:
        print("Client disconnected.")

async def main():
    async with websockets.serve(handle_audio, "localhost", 8765):
        print("Server started at ws://localhost:8765")
        await asyncio.Future()  # Run forever

asyncio.run(main())
