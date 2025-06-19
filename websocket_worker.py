import asyncio
import websockets
from media_stream import stream_handler

async def main():
    async with websockets.serve(stream_handler, "0.0.0.0", 10000):
        print("WebSocket server running on port 10000")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
