import pytest
from fastapi.testclient import TestClient
from fastapi import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from messaging_api.main import app
from messaging_api.crud import delete_user
from messaging_api.database import Base, SQLALCHEMY_DATABASE_URL


client = TestClient(app)

TEST_USER_ID = 999
TEST_MESSAGE_ID: int | None = None
TEST_MESSAGE_CONTENT: str = "I don't have enough imagination :)"
TEST_USERNAME = 'john_doe'
TEST_PASSWORD = 'superpassword'


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_user():
    response = client.post(
        url='/users/',
        json={
            'id': TEST_USER_ID,
            'username': TEST_USERNAME,
            'password': TEST_PASSWORD
        }
    )
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert all(['username', 'id' in response_json])
    assert response_json['username'] == TEST_USERNAME


def test_create_message():
    response = client.post(
        url=f'/users/{TEST_USER_ID}/messages/',
        json={'content': TEST_MESSAGE_CONTENT},
        headers={'username': TEST_USERNAME, 'password': TEST_PASSWORD}
    )
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert all(['id', 'content', 'user_id', 'created' in response_json])
    assert response_json['content'] == TEST_MESSAGE_CONTENT
    assert response_json['user_id'] == TEST_USER_ID


def test_message_retrieval():
    response = client.get(
        url=f'/messages/', params={'user_id': TEST_USER_ID},
        headers={'username': TEST_USERNAME, 'password': TEST_PASSWORD}
    )
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert all([
        all(['id', 'content', 'user_id', 'created' in message])
        for message in response_json
    ])


def test_cleanup(db_session):
    # Deleting test user (messages will nbe deleted as well, using cascade)
    delete_user(db_session, TEST_USER_ID)
