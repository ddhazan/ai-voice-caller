import asyncio
import websockets
from media_stream import stream_handler

# Reject Render's health check HTTP requests (HEAD / or GET /)
async def reject_http(path, request_headers):
    if "Upgrade" not in request_headers:
        return (
            400,
            [("Content-Type", "text/plain")],
            b"This endpoint only accepts WebSocket connections.\\n"
        )

async def main():
    print("✅ WebSocket server running on port 10000...")
    async with websockets.serve(
        stream_handler,
        host="0.0.0.0",
        port=10000,
        process_request=reject_http
    ):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
