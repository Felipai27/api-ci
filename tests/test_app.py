# tests/test_app.py

import sys
import os
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# adiciona a pasta-pai (onde está app.py) ao início do sys.path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
)
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

import pytest
from app import app  # agora deve encontrar app.py corretamente

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_home(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.get_json() == {"mensagem": "API de Presentes rodando com sucesso!"}

def test_listar_presente_inicial(client):
    resp = client.get("/presentes")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert any(p["id"] == 1 and p["nome"] == "Bicicleta" for p in data)

def test_crud_completo(client):
    # CREATE
    novo = {"nome": "Boneca", "preco": 120.5}
    r = client.post("/presentes", json=novo)
    assert r.status_code == 201
    criado = r.get_json()
    pid = criado["id"]

    # READ
    r = client.get(f"/presentes/{pid}")
    assert r.status_code == 200
    assert r.get_json()["nome"] == "Boneca"

    # UPDATE
    r = client.put(f"/presentes/{pid}", json={"preco": 200.0})
    assert r.status_code == 200
    assert r.get_json()["preco"] == 200.0

    # LIST
    r = client.get("/presentes")
    assert any(p["id"] == pid for p in r.get_json())

    # DELETE
    r = client.delete(f"/presentes/{pid}")
    assert r.status_code == 200

    # READ após DELETE
    r = client.get(f"/presentes/{pid}")
    assert r.status_code == 404

def test_404_para_id_inexistente(client):
    r = client.get("/presentes/9999")
    assert r.status_code == 404
    assert "erro" in r.get_json()
