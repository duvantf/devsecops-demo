"""
Tests de seguridad y funcionalidad con pytest.
En DevSecOps, el codigo sin tests es un riesgo.
"""

import pytest
from src.app import greet, get_user_safe


def test_greet_returns_string():
    resultado = greet("Duvan")
    assert isinstance(resultado, str)


def test_greet_incluye_nombre():
    resultado = greet("Duvan")
    assert "Duvan" in resultado


def test_greet_no_vacio():
    resultado = greet("test")
    assert len(resultado) > 0


def test_sql_injection_no_ejecuta_codigo():
    """
    Verifica que un input malicioso no rompe la funcion segura.
    Un SQL injection clasico: ' OR '1'='1
    La funcion safe debe manejarlo sin error.
    """
    input_malicioso = "' OR '1'='1"
    try:
        get_user_safe(input_malicioso)
        assert True
    except Exception as e:
        pytest.fail(f"La funcion segura no deberia fallar con input malicioso: {e}")


def test_greet_con_caracteres_especiales():
    """
    Verifica que la funcion maneja caracteres especiales sin explotar.
    """
    resultado = greet("<script>alert('xss')</script>")
    assert isinstance(resultado, str)