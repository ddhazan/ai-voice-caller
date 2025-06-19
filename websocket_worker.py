import asyncio
import websockets
from media_stream import stream_handler

async def reject_http(path, request_headers):
    # Render sends HTTP HEAD/GET health checks — reject them
    if "Upgrade" not in request_headers:
        return (
            400,
            [("Content-Type", "text/plain")],
            b"This endpoint only accepts WebSocket connections.\n"
        )

async def main():
    print("✅ WebSocket server running on port 10000...")
    async with websockets.serve(
        stream_handler,
        host="0.0.0.0",
        port=10000,
        process_request=reject_http  # 🔐 This blocks non-WS requests
    ):
        await asyncio.Future()  # Keep running forever

if __name__ == "__main__":
    asyncio.run(main())
