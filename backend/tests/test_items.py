import pytest
import requests

BASE_URL = "http://localhost:8000/api"

@pytest.fixture(scope="session", autouse=True)
def check_environment():
    """Check if the backend is running and in development mode before running any tests"""
    try:
        response = requests.get(f"{BASE_URL}/items/environment")
        if response.status_code != 200:
            pytest.exit("Backend server is not responding correctly")
        
        env = response.text.strip('"')  # FastAPI wraps strings in quotes
        if env != "development":
            pytest.exit(f"Backend is not in development mode. Current environment: {env}")
    except requests.ConnectionError:
        pytest.exit("Cannot connect to backend server. Is it running at localhost:8000?")

def test_create_and_delete_item():
    # Test creating an item
    item_data = {
        "title": "Test Item",
        "description": "Test Description",
        "is_active": True
    }
    
    # Create item
    response = requests.post(f"{BASE_URL}/items/", json=item_data)
    assert response.status_code == 201
    created_item = response.json()
    assert created_item["title"] == item_data["title"]
    assert created_item["description"] == item_data["description"]
    assert created_item["is_active"] == item_data["is_active"]
    
    # Clean up - delete the item
    item_id = created_item["id"]
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    assert response.status_code == 204

def test_create_read_update_delete_flow():
    # Create an item
    item_data = {
        "title": "CRUD Test Item",
        "description": "Test CRUD operations",
        "is_active": True
    }
    
    # Create
    response = requests.post(f"{BASE_URL}/items/", json=item_data)
    assert response.status_code == 201
    created_item = response.json()
    item_id = created_item["id"]
    
    # Read
    response = requests.get(f"{BASE_URL}/items/{item_id}")
    assert response.status_code == 200
    retrieved_item = response.json()
    assert retrieved_item == created_item
    
    # Update
    update_data = {
        "title": "Updated CRUD Test Item",
        "is_active": False
    }
    response = requests.put(f"{BASE_URL}/items/{item_id}", json=update_data)
    assert response.status_code == 200
    updated_item = response.json()
    assert updated_item["title"] == update_data["title"]
    assert updated_item["is_active"] == update_data["is_active"]
    assert updated_item["description"] == item_data["description"]  # Unchanged
    
    # Delete
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    assert response.status_code == 204

def test_list_items():
    # Create two items
    items_data = [
        {"title": "List Item 1", "description": "First test item", "is_active": True},
        {"title": "List Item 2", "description": "Second test item", "is_active": True}
    ]
    
    created_items = []
    for item_data in items_data:
        response = requests.post(f"{BASE_URL}/items/", json=item_data)
        assert response.status_code == 201
        created_items.append(response.json())
    
    # Get list of items
    response = requests.get(f"{BASE_URL}/items/")
    assert response.status_code == 200
    items_list = response.json()
    
    # Verify our items are in the list
    created_ids = {item["id"] for item in created_items}
    found_items = [item for item in items_list if item["id"] in created_ids]
    assert len(found_items) == len(created_items)
    
    # Clean up - delete created items
    for item in created_items:
        response = requests.delete(f"{BASE_URL}/items/{item['id']}")
        assert response.status_code == 204

def test_batch_operations():
    # Test batch create
    items_to_create = {
        "items": [
            {"title": "Batch Item 1", "description": "First batch item", "is_active": True},
            {"title": "Batch Item 2", "description": "Second batch item", "is_active": True}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/items/batch", json=items_to_create)
    print(f"Batch create response: {response.text}")  # Print the full response for debugging
    assert response.status_code == 201
    batch_result = response.json()
    assert len(batch_result["success"]) == 2
    assert len(batch_result["failed"]) == 0
      # Get the created item IDs
    created_ids = [item["id"] for item in batch_result["success"]]
    print(f"Created IDs: {created_ids}")  # Debug print
    
    # Test batch delete
    delete_data = {"item_ids": created_ids}
    print(f"Delete request data: {delete_data}")  # Debug print
    response = requests.delete(f"{BASE_URL}/items/batch", json=delete_data)
    print(f"Delete response: {response.text}")  # Debug print
    assert response.status_code == 200
    delete_result = response.json()
    assert len(delete_result["success"]) == 2
    assert len(delete_result["failed"]) == 0

def test_item_not_found():
    # Try to get a non-existent item
    response = requests.get(f"{BASE_URL}/items/99999")
    assert response.status_code == 404
    
    # Try to update a non-existent item
    update_data = {"name": "Non-existent Item"}
    response = requests.put(f"{BASE_URL}/items/99999", json=update_data)
    assert response.status_code == 404
    
    # Try to delete a non-existent item
    response = requests.delete(f"{BASE_URL}/items/99999")
    assert response.status_code == 404
