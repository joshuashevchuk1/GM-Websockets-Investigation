import asyncio
import websockets
import sounddevice as sd
import numpy as np
import queue

RATE = 16000
CHUNK_DURATION = 1  # seconds
CHUNK_SIZE = int(RATE * CHUNK_DURATION)
CHANNELS = 1

send_queue = queue.Queue()
recv_queue = asyncio.Queue()

def audio_callback(indata, frames, time, status):
    # Called in a separate thread by sounddevice — push to thread-safe queue
    send_queue.put(indata.copy())

async def sender(websocket):
    while True:
        if not send_queue.empty():
            audio_chunk = send_queue.get()
            await websocket.send(audio_chunk.tobytes())
            print("Sent chunk to server")
        await asyncio.sleep(0.01)  # slight pause to yield control

async def receiver(websocket):
    while True:
        echoed_data = await websocket.recv()
        print("Received echoed chunk")
        audio_np = np.frombuffer(echoed_data, dtype='int16')
        await recv_queue.put(audio_np)

async def player():
    while True:
        chunk = await recv_queue.get()
        sd.play(chunk, samplerate=RATE)
        sd.wait()

async def record_and_stream():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Connected to server")

        # Start recording from microphone
        with sd.InputStream(samplerate=RATE, channels=CHANNELS, dtype='int16',
                            blocksize=CHUNK_SIZE, callback=audio_callback):
            await asyncio.gather(
                sender(websocket),
                receiver(websocket),
                player()
            )

asyncio.run(record_and_stream())
