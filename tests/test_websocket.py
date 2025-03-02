import pytest
import json
import websockets
from httpx import AsyncClient

WS_URL = "ws://127.0.0.1:8555/ws/tasks"
API_URL = "http://127.0.0.1:8555/tasks/"


@pytest.mark.asyncio
async def test_websocket():
    async with websockets.connect(WS_URL) as websocket:
        initial_data = await websocket.recv()
        initial_tasks = json.loads(initial_data)
        assert isinstance(initial_tasks, list)
        async with AsyncClient(base_url="http://127.0.0.1:8555") as client:
            response = await client.post(API_URL, json={"title": "Test WebSocket Task"})
            assert response.status_code == 200
            new_task = response.json()
        updated_data = await websocket.recv()
        updated_tasks = json.loads(updated_data)
        assert isinstance(updated_tasks, list)
        assert any(task["title"] == "Test WebSocket Task" for task in updated_tasks)
