from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from .. import models
from ..database import Base
from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from ..models import ToDos

SQLALCHEMY_DATABASE_URI = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'test', 'user_id': 1, 'role': 'admin'}


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = ToDos(
        title='Test ToDo',
        description='Test ToDo',
        priority=5,
        completed=False,
        owner_id=1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


def test_read_all_authenticated(test_todo):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'id': test_todo.id,
        'title': test_todo.title,
        'description': test_todo.description,
        'priority': test_todo.priority,
        'completed': test_todo.completed,
        'owner_id': test_todo.owner_id
    }]


def test_read_one_authenticated(test_todo):
    response = client.get(f'/todo/{test_todo.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': test_todo.id,
        'title': 'Test ToDo',
        'description': 'Test ToDo',
        'priority': 5,
        'completed': False,
        'owner_id': 1
    }


def test_read_one_authenticated_fail(test_todo):
    response = client.get(f'/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'ToDo not found'}


def test_create_todo(test_todo):
    response_data = {
        'title': 'Test ToDo',
        'description': 'Test ToDo',
        'priority': 5,
        'completed': False,
    }
    response = client.post('/todo', json=response_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(models.ToDos).filter(models.ToDos.id == 2).first()
    assert model.title == response_data['title']
    assert model.description == response_data['description']
    assert model.priority == response_data['priority']
    assert model.completed == response_data['completed']