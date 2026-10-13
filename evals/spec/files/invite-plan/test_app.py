from app import app


def test_team_page():
    assert app.test_client().get('/teams/1').status_code == 200
