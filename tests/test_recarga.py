"""
Tests unitarios - RecargaYa S.A.S.
Partición de equivalencia + valores límite
TDD Ciclo 1 - RED
"""
import pytest
from app.recarga import calcular_recarga


# ─── PARTICIÓN DE EQUIVALENCIA: montos inválidos ───────────────────────────────

def test_monto_menor_al_minimo_es_rechazado():
    resultado = calcular_recarga(500)
    assert resultado["valido"] is False
    assert "rechazado" in resultado["mensaje"].lower()


def test_monto_mayor_al_maximo_es_rechazado():
    resultado = calcular_recarga(60000)
    assert resultado["valido"] is False
    assert "rechazado" in resultado["mensaje"].lower()


def test_monto_cero_es_rechazado():
    resultado = calcular_recarga(0)
    assert resultado["valido"] is False


# ─── VALORES LÍMITE ────────────────────────────────────────────────────────────

def test_limite_inferior_valido_1000():
    resultado = calcular_recarga(1000)
    assert resultado["valido"] is True


def test_limite_inferior_invalido_999():
    resultado = calcular_recarga(999)
    assert resultado["valido"] is False


def test_limite_superior_valido_50000():
    resultado = calcular_recarga(50000)
    assert resultado["valido"] is True


def test_limite_superior_invalido_50001():
    resultado = calcular_recarga(50001)
    assert resultado["valido"] is False


# ─── PARTICIÓN: sin bonificación ($1.000 – $9.999) ────────────────────────────

def test_recarga_sin_bonificacion():
    resultado = calcular_recarga(5000)
    assert resultado["valido"] is True
    assert resultado["bonificacion_porcentaje"] == 0


# ─── PARTICIÓN: bonificación 10% ($10.000 – $29.999) ─────────────────────────

def test_recarga_con_bonificacion_10_porciento():
    resultado = calcular_recarga(10000)
    assert resultado["valido"] is True
    assert resultado["bonificacion_porcentaje"] == 10


def test_recarga_limite_inferior_bonificacion_10():
    resultado = calcular_recarga(10000)
    assert resultado["bonificacion_porcentaje"] == 10


def test_recarga_justo_antes_de_25_porciento():
    resultado = calcular_recarga(29999)
    assert resultado["bonificacion_porcentaje"] == 10


# ─── PARTICIÓN: bonificación 25% ($30.000 en adelante) ───────────────────────

def test_recarga_con_bonificacion_25_porciento():
    resultado = calcular_recarga(30000)
    assert resultado["valido"] is True
    assert resultado["bonificacion_porcentaje"] == 25


def test_recarga_50000_bonificacion_25_porciento():
    resultado = calcular_recarga(50000)
    assert resultado["bonificacion_porcentaje"] == 25


# ─── USUARIO PREMIUM ──────────────────────────────────────────────────────────

def test_usuario_premium_sin_bonificacion_base_suma_5():
    resultado = calcular_recarga(5000, premium=True)
    assert resultado["bonificacion_porcentaje"] == 5


def test_usuario_premium_con_bonificacion_10_suma_5():
    resultado = calcular_recarga(10000, premium=True)
    assert resultado["bonificacion_porcentaje"] == 15


def test_usuario_premium_con_bonificacion_25_suma_5():
    resultado = calcular_recarga(30000, premium=True)
    assert resultado["bonificacion_porcentaje"] == 30


def test_usuario_no_premium_no_suma_5():
    resultado = calcular_recarga(30000, premium=False)
    assert resultado["bonificacion_porcentaje"] == 25


def test_monto_invalido_premium_sigue_rechazado():
    resultado = calcular_recarga(500, premium=True)
    assert resultado["valido"] is False
