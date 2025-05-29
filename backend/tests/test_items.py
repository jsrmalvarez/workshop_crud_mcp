import pytest
import requests

BASE_URL = "http://localhost:8000/api"

def test_create_and_delete_item():
    # Test creating an item
    item_data = {
        "name": "Test Item",
        "description": "Test Description",
        "price": 10.99
    }
    
    # Create item
    response = requests.post(f"{BASE_URL}/items/", json=item_data)
    assert response.status_code == 201
    created_item = response.json()
    assert created_item["name"] == item_data["name"]
    assert created_item["description"] == item_data["description"]
    assert created_item["price"] == item_data["price"]
    
    # Clean up - delete the item
    item_id = created_item["id"]
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    assert response.status_code == 204

def test_create_read_update_delete_flow():
    # Create an item
    item_data = {
        "name": "CRUD Test Item",
        "description": "Test CRUD operations",
        "price": 15.99
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
        "name": "Updated CRUD Test Item",
        "price": 20.99
    }
    response = requests.put(f"{BASE_URL}/items/{item_id}", json=update_data)
    assert response.status_code == 200
    updated_item = response.json()
    assert updated_item["name"] == update_data["name"]
    assert updated_item["price"] == update_data["price"]
    assert updated_item["description"] == item_data["description"]  # Unchanged
    
    # Delete
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    assert response.status_code == 204

def test_list_items():
    # Create two items
    items_data = [
        {"name": "List Item 1", "description": "First test item", "price": 10.99},
        {"name": "List Item 2", "description": "Second test item", "price": 20.99}
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
            {"name": "Batch Item 1", "description": "First batch item", "price": 10.99},
            {"name": "Batch Item 2", "description": "Second batch item", "price": 20.99}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/items/batch", json=items_to_create)
    assert response.status_code == 201
    batch_result = response.json()
    assert len(batch_result["success"]) == 2
    assert len(batch_result["failed"]) == 0
    
    # Get the created item IDs
    created_ids = [item["id"] for item in batch_result["success"]]
    
    # Test batch delete
    delete_data = {"item_ids": created_ids}
    response = requests.delete(f"{BASE_URL}/items/batch", json=delete_data)
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
