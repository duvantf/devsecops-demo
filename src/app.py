"""
DevSecOps Demo - App simple en Python
Contiene una vulnerabilidad INTENCIONAL de SQL Injection en get_user().
NO usar get_user() en producción.
"""

import sqlite3
import html
import os
import warnings

# Ruta absoluta a la BD, relativa a este archivo
DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")


def get_user(username: str):
    """
    ⚠️  VULNERABLE: SQL Injection por concatenación de strings.
    Semgrep con p/bandit debería detectar esto.
    Solo existe para fines de demostración DevSecOps.
    """
    warnings.warn(
        "get_user() es VULNERABLE a SQL Injection. Solo usar en demos.",
        DeprecationWarning,
        stacklevel=2,
    )
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # MAL: nunca concatenes input del usuario en SQL
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        return cursor.fetchone()


def get_user_safe(username: str):
    """
    ✅ Versión segura usando parámetros preparados.
    Evita SQL Injection correctamente.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # BIEN: parámetros preparados evitan SQL Injection
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone()


def greet(name: str) -> str:
    """
    Saluda al usuario escapando caracteres HTML para evitar XSS.
    """
    safe_name = html.escape(name)
    return f"Hola, {safe_name}! Bienvenido al demo DevSecOps."


if __name__ == "__main__":
    print(greet("mundo"))