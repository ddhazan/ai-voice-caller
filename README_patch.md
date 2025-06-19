### 🛠️ Post-Update Instructions

1. Replace your existing `media_stream.py` with this new version.
2. Re-deploy the app on Render.
3. Ensure the `/media` WebSocket route is mapped to this handler:

In `app.py` add:

```python
from media_stream import stream_handler
import asyncio

@app.route("/media")
def media_route():
    return Response("Media route is for WebSocket only", 400)

def start_websocket():
    return websockets.serve(stream_handler, "0.0.0.0", 10000)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_websocket())
    app.run(host="0.0.0.0", port=10000)
```

4. You may need to expose port 10000 using a Render background worker or use a TCP-compatible deployment like Fly.io if WebSocket over HTTP fails on Render free tier.