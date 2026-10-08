from common.model.Models import db, Users
from werkzeug.security import generate_password_hash, check_password_hash

def test_create_and_fetch_user(test_client):
    
    new_user = Users(username="ci_cd_tester", password="supersecret", role="user")
    db.session.add(new_user)
    db.session.commit()
    
    fetched_user = Users.query.filter_by(username="ci_cd_tester").first()
    
    assert fetched_user is not None
    assert fetched_user.username == "ci_cd_tester"
    assert fetched_user.role == "user"

def test_encrypt_user_password(test_client):
    password = "Hell0"
    password_encrypted = generate_password_hash(password)
    new_user = Users(username="ci_cd_tester_2", password=password_encrypted, role="user")
    db.session.add(new_user)
    db.session.commit()

    fetched_user = Users.query.filter_by(username="ci_cd_tester_2").first()

    assert fetched_user is not None

    assert fetched_user.password == password_encrypted
    assert check_password_hash(fetched_user.password, password)

    assert not check_password_hash(fetched_user.password, "Hel1o")


