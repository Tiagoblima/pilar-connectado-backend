import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/v1/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


if __name__ == '__main__':
    unittest.main()
