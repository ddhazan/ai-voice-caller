import asyncio
import websockets
from media_stream import stream_handler

async def main():
    print("Starting WebSocket server...")
    async with websockets.serve(
        stream_handler,
        host="0.0.0.0",
        port=10000,
        process_request=reject_non_websocket_requests
    ):
        await asyncio.Future()  # Keep running

async def reject_non_websocket_requests(path, request_headers):
    # Render health checks send regular HTTP requests — reject them cleanly
    if "Upgrade" not in request_headers:
        return (400, [], b"Expected WebSocket upgrade")

if __name__ == "__main__":
    asyncio.run(main())
