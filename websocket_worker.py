import asyncio
import websockets
from media_stream import stream_handler

# This tells Render "don't treat this like HTTP"
async def reject_http(path, request_headers):
    if "Upgrade" not in request_headers:
        return (400, [], b"Expected WebSocket upgrade")

async def main():
    print("✅ WebSocket server running on port 10000...")
    async with websockets.serve(
        stream_handler,
        host="0.0.0.0",
        port=10000,
        process_request=reject_http  # Add this!
    ):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
