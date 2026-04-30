import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestIntegration:
    def setup_method(self):
        client.delete("/users")
    
    def test_full_user_lifecycle(self):
        create_response = client.post("/users", json={
            "username": "lifecycle_test",
            "age": 28
        })
        assert create_response.status_code == 201
        user_id = create_response.json()["id"]
        
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 200
        assert get_response.json()["username"] == "lifecycle_test"
        
        update_response = client.put(f"/users/{user_id}", json={
            "username": "updated_name",
            "age": 35
        })
        assert update_response.status_code == 200
        assert update_response.json()["username"] == "updated_name"
        
        get2_response = client.get(f"/users/{user_id}")
        assert get2_response.json()["username"] == "updated_name"
        
        delete_response = client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 204
        
        get3_response = client.get(f"/users/{user_id}")
        assert get3_response.status_code == 404
    
    def test_multiple_users_operations(self):
        users = []
        for i in range(3):
            response = client.post("/users", json={
                "username": f"user_{i}",
                "age": 20 + i
            })
            assert response.status_code == 201
            users.append(response.json())
        
        all_users = client.get("/users")
        assert len(all_users.json()) == 3
        
        delete_response = client.delete(f"/users/{users[1]['id']}")
        assert delete_response.status_code == 204
        
        remaining = client.get("/users")
        assert len(remaining.json()) == 2
        
        remaining_ids = [u["id"] for u in remaining.json()]
        assert users[0]["id"] in remaining_ids
        assert users[2]["id"] in remaining_ids
        assert users[1]["id"] not in remaining_ids