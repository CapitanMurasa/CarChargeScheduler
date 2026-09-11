import pytest
from Main import app 
from common.model.Models import db

@pytest.fixture
def test_client():
    app.config["TESTING"] = True
    
    with app.app_context():
        db.create_all()
        
        with app.test_client() as client:
            yield client
            
        db.session.remove()
        db.drop_all()