from common.model.Models import db, Users

def test_create_and_fetch_user(test_client):
    
    new_user = Users(username="ci_cd_tester", password="supersecret", role="user")
    db.session.add(new_user)
    db.session.commit()
    
    fetched_user = Users.query.filter_by(username="ci_cd_tester").first()
    
    assert fetched_user is not None
    assert fetched_user.username == "ci_cd_tester"
    assert fetched_user.role == "user"