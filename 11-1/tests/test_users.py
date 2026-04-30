import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestUserAPI:
    def setup_method(self):
        client.delete("/users")
    
    def test_create_user_success(self):
        response = client.post("/users", json={
            "username": "ivan123",
            "age": 25
        })
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["username"] == "ivan123"
        assert data["age"] == 25
    
    def test_create_user_invalid_data(self):
        response = client.post("/users", json={
            "username": "",
            "age": -5
        })

        assert response.status_code == 422
    
    def test_get_user_success(self):
        create_response = client.post("/users", json={
            "username": "petr456",
            "age": 30
        })
        user_id = create_response.json()["id"]
        
        response = client.get(f"/users/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "petr456"
        assert data["age"] == 30
    
    def test_get_user_not_found(self):
        response = client.get("/users/99999")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"]
    
    def test_get_all_users(self):
        client.post("/users", json={"username": "user1", "age": 20})
        client.post("/users", json={"username": "user2", "age": 25})
        
        response = client.get("/users")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_update_user_success(self):
        create_response = client.post("/users", json={
            "username": "old_name",
            "age": 20
        })
        user_id = create_response.json()["id"]
        
        response = client.put(f"/users/{user_id}", json={
            "username": "new_name",
            "age": 25
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "new_name"
        assert data["age"] == 25
    
    def test_update_user_not_found(self):
        response = client.put("/users/99999", json={
            "username": "test",
            "age": 30
        })
        
        assert response.status_code == 404
    
    def test_update_user_partial(self):
        create_response = client.post("/users", json={
            "username": "original",
            "age": 25
        })
        user_id = create_response.json()["id"]
        
        response = client.put(f"/users/{user_id}", json={
            "username": "updated_only_name"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "updated_only_name"
        assert data["age"] == 25
    
    def test_delete_user_success(self):
        create_response = client.post("/users", json={
            "username": "to_delete",
            "age": 30
        })
        user_id = create_response.json()["id"]
        
        response = client.delete(f"/users/{user_id}")
        
        assert response.status_code == 204
        
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404
    
    def test_delete_user_not_found(self):
        response = client.delete("/users/99999")
        
        assert response.status_code == 404
    
    def test_create_two_users_unique_ids(self):
        user1 = client.post("/users", json={"username": "user1", "age": 20})
        user2 = client.post("/users", json={"username": "user2", "age": 25})
        
        assert user1.status_code == 201
        assert user2.status_code == 201
        
        id1 = user1.json()["id"]
        id2 = user2.json()["id"]
        
        assert id1 != id2