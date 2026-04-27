import pytest
import sqlite3
from src.app import greet, get_user_safe


@pytest.fixture(autouse=True)
def setup_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT
        )
    """)

    conn.commit()
    conn.close()


def test_greet_returns_string():
    assert isinstance(greet("Duvan"), str)


def test_greet_incluye_nombre():
    assert "Duvan" in greet("Duvan")


def test_greet_no_vacio():
    assert len(greet("test")) > 0


def test_sql_injection_no_ejecuta_codigo():
    input_malicioso = "' OR '1'='1"
    resultado = get_user_safe(input_malicioso)
    assert resultado is not None


def test_greet_con_caracteres_especiales():
    resultado = greet("<script>alert('xss')</script>")
    assert isinstance(resultado, str)
    assert len(resultado) > 0