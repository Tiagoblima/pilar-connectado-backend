import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/v1/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_get_opportunity():
    response = client.get("/v1/opportunity/")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_post_opportunity():
    response = client.post(
        "/v1/opportunity/",
        json={"id_portomember": 1, "startDate": "10/11/2021",
              "endDate": "20/11/2021", "isactive": "True",
              "description": "Serviço de construção civil",
              "id_skill": "1", "value": 500
              },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 4, "id_portomember": 1, "startDate": "10/11/2021",
        "endDate": "20/11/2021", "isactive": True,
        "description": "Serviço de construção civil",
        "id_skill": 1, "value": 500.0
    }


def test_get_previous_match_members():
    response = client.get("/v1/previous_match_members/")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_post_previous_match_members():
    response = client.post(
        "/v1/previous_match_member/",
        json={"id": 3, "id_match": 3,
              "id_match_user": 1,
              "porto_member_user_id": 6
              },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 3,
        "id_match": 3,
        "id_match_user": 1,
        "porto_member_user_id": 6
    }


if __name__ == '__main__':
    unittest.main()
