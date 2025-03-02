import asyncio
import websockets


async def test_websocket():
    uri = "ws://127.0.0.1:8555/ws/tasks"

    async with websockets.connect(uri) as websocket:
        print("Connection to WebSocket!")

        initial_data = await websocket.recv()
        print(f"Received Data: {initial_data}")

        while True:
            try:
                message = await websocket.recv()
                print(f"Updated: {message}")
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break


asyncio.run(test_websocket())
