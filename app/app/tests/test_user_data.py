import pytest
from app.patterns.user_data_template import WebUserDataCollector
from app.patterns.data_storage_factory import SQLiteStorageFactory
import os

@pytest.fixture
def storage():
    """Fixture to create a test database"""
    db_path = "test_data.db"
    factory = SQLiteStorageFactory(db_path)
    storage = factory.create_storage()
    yield storage
    # Cleanup after tests
    if os.path.exists(db_path):
        os.remove(db_path)

def test_user_data_collection():
    """Test the collection of user data"""
    collector = WebUserDataCollector()
    
    # Test data
    collector.user_data["name"] = "Test User"
    collector.user_data["interests"] = ["Python", "Machine Learning"]
    collector.user_data["experience_level"] = "intermediate"
    
    data = collector.get_user_data()
    assert data["name"] == "Test User"
    assert "Python" in data["interests"]
    assert data["experience_level"] == "intermediate"

def test_data_storage(storage):
    """Test storing and retrieving user data"""
    test_data = {
        "name": "Test User",
        "interests": ["Python", "Machine Learning"],
        "experience_level": "intermediate"
    }
    
    # Store data
    user_id = storage.save_user(test_data)
    assert user_id is not None
    
    # Retrieve data
    stored_data = storage.get_user(user_id)
    assert stored_data["name"] == test_data["name"]
    assert stored_data["interests"] == test_data["interests"]

def test_invalid_user_data():
    """Test validation of user data"""
    collector = WebUserDataCollector()
    
    # Test empty name
    with pytest.raises(ValueError, match="User name cannot be empty"):
        collector.get_user_data()
