"""
Tests de integración - API REST RecargaYa
TDD Ciclo 2 - RED
"""
import pytest
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


# ─── ENDPOINT POST /recargar ───────────────────────────────────────────────────

def test_api_recarga_valida_sin_premium():
    response = client.post("/recargar", json={"monto": 5000, "premium": False})
    assert response.status_code == 200
    data = response.json()
    assert data["valido"] is True
    assert data["bonificacion_porcentaje"] == 0


def test_api_recarga_valida_con_bonificacion_10():
    response = client.post("/recargar", json={"monto": 15000, "premium": False})
    assert response.status_code == 200
    data = response.json()
    assert data["valido"] is True
    assert data["bonificacion_porcentaje"] == 10


def test_api_recarga_valida_con_bonificacion_25():
    response = client.post("/recargar", json={"monto": 30000, "premium": False})
    assert response.status_code == 200
    data = response.json()
    assert data["valido"] is True
    assert data["bonificacion_porcentaje"] == 25


def test_api_recarga_premium_suma_5():
    response = client.post("/recargar", json={"monto": 30000, "premium": True})
    assert response.status_code == 200
    data = response.json()
    assert data["bonificacion_porcentaje"] == 30


def test_api_recarga_monto_invalido_devuelve_400():
    response = client.post("/recargar", json={"monto": 500, "premium": False})
    assert response.status_code == 400
    data = response.json()
    assert "rechazado" in data["detail"].lower()


def test_api_recarga_monto_sobre_maximo_devuelve_400():
    response = client.post("/recargar", json={"monto": 100000, "premium": False})
    assert response.status_code == 400


def test_api_premium_por_defecto_es_false():
    response = client.post("/recargar", json={"monto": 10000})
    assert response.status_code == 200
    assert response.json()["bonificacion_porcentaje"] == 10


# ─── ENDPOINT GET /health ──────────────────────────────────────────────────────

def test_api_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
