import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

@pytest.mark.asyncio
async def test_create_and_get_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Создание
        create_response = await ac.post("/tasks", json={
            "title": "Тестовая задача",
            "description": "Описание",
            "priority": "high"
        })
        assert create_response.status_code == 200
        task_id = create_response.json()["id"]
        
        # Получение
        get_response = await ac.get(f"/tasks/{task_id}")
        assert get_response.status_code == 200
        assert get_response.json()["title"] == "Тестовая задача"

@pytest.mark.asyncio
async def test_list_tasks():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_update_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Создаём
        create = await ac.post("/tasks", json={"title": "Старое"})
        task_id = create.json()["id"]
        
        # Обновляем
        update = await ac.put(f"/tasks/{task_id}", json={
            "title": "Новое",
            "description": "Новое описание",
            "priority": "low"
        })
        assert update.status_code == 200
        
        # Проверяем
        get = await ac.get(f"/tasks/{task_id}")
        assert get.json()["title"] == "Новое"

@pytest.mark.asyncio
async def test_update_status():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create = await ac.post("/tasks", json={"title": "Задача"})
        task_id = create.json()["id"]
        
        response = await ac.patch(f"/tasks/{task_id}/status", json={"status": "completed"})
        assert response.status_code == 200
        
        get = await ac.get(f"/tasks/{task_id}")
        assert get.json()["status"] == "completed"

@pytest.mark.asyncio
async def test_delete_task():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create = await ac.post("/tasks", json={"title": "Для удаления"})
        task_id = create.json()["id"]
        
        delete = await ac.delete(f"/tasks/{task_id}")
        assert delete.status_code == 200
        
        get = await ac.get(f"/tasks/{task_id}")
        assert get.status_code == 404