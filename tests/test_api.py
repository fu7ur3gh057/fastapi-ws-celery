import pytest
from httpx import AsyncClient

BASE_URL = "http://127.0.0.1:8555"
API_URL = f"{BASE_URL}/tasks"


@pytest.mark.asyncio
async def test_read_tasks():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/tasks/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_task():
    async with AsyncClient(base_url=BASE_URL) as client:
        task_data = {"title": "Test Task"}
        response = await client.post("/tasks/", json=task_data)
        assert response.status_code == 200
        new_task = response.json()
        assert new_task["title"] == "Test Task"
        assert "id" in new_task


@pytest.mark.asyncio
async def test_read_task():
    async with AsyncClient(base_url=BASE_URL) as client:
        task_data = {"title": "Single Task"}
        create_response = await client.post("/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        response = await client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        task = response.json()
        assert task["id"] == task_id
        assert task["title"] == "Single Task"


@pytest.mark.asyncio
async def test_update_task():
    async with AsyncClient(base_url=BASE_URL) as client:
        task_data = {"title": "Old Task"}
        create_response = await client.post("/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        update_data = {"title": "Updated Task", "completed": True}
        response = await client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == 200
        updated_task = response.json()
        assert updated_task["title"] == "Updated Task"
        assert updated_task["completed"] is True


@pytest.mark.asyncio
async def test_delete_task():
    async with AsyncClient(base_url=BASE_URL) as client:
        task_data = {"title": "Task to delete"}
        create_response = await client.post("/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        response = await client.delete(f"/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Task deleted"

        response = await client.get(f"/tasks/{task_id}")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_send_report():
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/tasks/send-report", params={"email": "test@example.com"})
        assert response.status_code == 200
        task_data = response.json()
        assert "task_id" in task_data
        assert task_data["message"] == "Report is being sent to test@example.com"
