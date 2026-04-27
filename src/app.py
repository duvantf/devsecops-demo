"""
DevSecOps Demo - App simple en Python
Vulnerabilidad corregida: SQL Injection eliminado.
"""

import sqlite3


def get_user(username: str):
    """
    Version segura usando parametros preparados.
    Ya no hay SQL injection.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # BIEN: parametros preparados evitan SQL injection
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()


def greet(name: str) -> str:
    return f"Hola, {name}! Bienvenido al demo DevSecOps."


if __name__ == "__main__":
    print(greet("mundo"))