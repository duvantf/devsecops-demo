"""
DevSecOps Demo - App simple en Python
Contiene una vulnerabilidad intencional de SQL Injection.
"""

import sqlite3


def get_user(username: str):
    """
    VULNERABLE: SQL Injection por concatenacion de strings.
    Semgrep con p/bandit deberia detectar esto.
    """
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # MAL: nunca concatenes input del usuario en SQL
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()


def get_user_safe(username: str):
    """
    Version segura usando parametros preparados.
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