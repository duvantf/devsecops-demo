import pytest
import sqlite3
import os
from src.app import greet, get_user_safe, DB_PATH


@pytest.fixture(autouse=True)
def setup_db():
    """
    Crea la BD de prueba antes de cada test y la limpia después.
    Usa la misma ruta (DB_PATH) que las funciones en app.py.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT
        )
    """)
    cursor.execute("INSERT INTO users (username) VALUES (?)", ("admin",))
    conn.commit()
    conn.close()

    yield  # aquí corren los tests

    # Teardown: limpiar la BD después de cada test
    conn2 = sqlite3.connect(DB_PATH)
    conn2.execute("DROP TABLE IF EXISTS users")
    conn2.commit()
    conn2.close()


# ── Tests de greet ────────────────────────────────────────────

def test_greet_returns_string():
    assert isinstance(greet("Duvan"), str)


def test_greet_incluye_nombre():
    assert "Duvan" in greet("Duvan")


def test_greet_no_vacio():
    assert len(greet("test")) > 0


def test_greet_escapa_xss():
    """Verifica que greet() no devuelva tags HTML sin escapar."""
    resultado = greet("<script>alert('xss')</script>")
    assert isinstance(resultado, str)
    assert len(resultado) > 0
    assert "<script>" not in resultado  # ✅ verifica sanitización real
    assert "&lt;script&gt;" in resultado


# ── Tests de SQL Injection ────────────────────────────────────

def test_sql_injection_no_rompe_sistema():
    """
    Con parámetros preparados, el input malicioso se trata como
    texto literal y no debe encontrar ningún usuario.
    """
    input_malicioso = "' OR '1'='1"
    resultado = get_user_safe(input_malicioso)
    assert resultado is None or resultado == []


def test_get_user_safe_encuentra_usuario_existente():
    """Verifica que la función sí retorna usuarios válidos."""
    resultado = get_user_safe("admin")
    assert resultado is not None
    assert resultado[1] == "admin"


def test_get_user_safe_retorna_none_si_no_existe():
    resultado = get_user_safe("usuario_que_no_existe")
    assert resultado is None