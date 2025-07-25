import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine
from app.server import app
from database.sqlmodel import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    veiculo_data = {
        "veiculo": "Carro Teste",
        "marca": "Toyota",
        "ano": 1999,
        "descricao": "Descrição do carro teste",
        "vendido": False,
    }
    client.post("/veiculos/", json=veiculo_data)
    yield client
    app.dependency_overrides.clear()


def test_list_veiculos(client: TestClient):
    response = client.get("/veiculos/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "pages" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


def test_create_veiculo(client: TestClient):
    veiculo_data = {
        "veiculo": "Carro",
        "marca": "Toyota",
        "ano": 2020,
        "descricao": "Um carro novo",
        "vendido": False,
    }
    response = client.post("/veiculos/", json=veiculo_data)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["veiculo"] == veiculo_data["veiculo"]
    assert data["marca"] == veiculo_data["marca"]
    assert data["ano"] == veiculo_data["ano"]
    assert data["descricao"] == veiculo_data["descricao"]
    assert data["vendido"] == veiculo_data["vendido"]
    assert data["created"] is not None
    assert data["updated"] is None


def test_create_veiculo_invalid(client: TestClient):
    veiculo_data = {
        "marca": "Toyota",
        "ano": 2020,
        "descricao": "Um carro novo",
    }
    response = client.post("/veiculos/", json=veiculo_data)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_get_veiculo(client: TestClient):
    response = client.get("/veiculos/1")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["id"] == 1
    assert data["veiculo"] == "Carro Teste"
    assert data["marca"] == "Toyota"
    assert data["ano"] == 1999
    assert data["descricao"] == "Descrição do carro teste"
    assert data["vendido"] is False


def test_get_veiculo_not_found(client: TestClient):
    response = client.get("/veiculos/999")
    assert response.status_code == 404
    data = response.json()
    assert data == {
        "code": "veiculo_not_found",
        "error": "Veículo com ID 999 não encontrado.",
    }


def test_update_veiculo(client: TestClient):
    update_data = {
        "veiculo": "Carro Atualizado",
        "marca": "Toyota",
        "ano": 2021,
        "descricao": "Descrição atualizada do carro teste",
        "vendido": True,
    }
    response = client.put("/veiculos/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["veiculo"] == update_data["veiculo"]
    assert data["marca"] == update_data["marca"]
    assert data["ano"] == update_data["ano"]
    assert data["descricao"] == update_data["descricao"]
    assert data["vendido"] is True


def test_update_veiculo_not_found(client: TestClient):
    update_data = {
        "veiculo": "Carro Inexistente",
        "marca": "Toyota",
        "ano": 2021,
        "descricao": "Descrição de um carro inexistente",
        "vendido": True,
    }
    response = client.put("/veiculos/999", json=update_data)
    assert response.status_code == 404
    data = response.json()
    assert data == {
        "code": "veiculo_not_found",
        "error": "Veículo com ID 999 não encontrado.",
    }


def test_patch_veiculo(client: TestClient):
    patch_data = {
        "vendido": True,
    }
    response = client.patch("/veiculos/1", json=patch_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["vendido"] is True


def test_patch_veiculo_not_found(client: TestClient):
    patch_data = {
        "vendido": True,
    }
    response = client.patch("/veiculos/999", json=patch_data)
    assert response.status_code == 404
    data = response.json()
    assert data == {
        "code": "veiculo_not_found",
        "error": "Veículo com ID 999 não encontrado.",
    }
