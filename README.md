# DevSecOps Demo — Python

![Pipeline DevSecOps](https://github.com/duvantf/devsecops-demo/actions/workflows/security.yml/badge.svg)

Proyecto práctico de aprendizaje DevSecOps construido desde cero.
Cada `git push` dispara un pipeline de seguridad automatizado en GitHub Actions.

---

## Evidencias del pipeline funcionando

### 1. Historial completo de runs
Cada commit disparó el pipeline automáticamente. Se ve la evolución del proyecto:
desde el primer intento fallido hasta todos los pasos en verde.

![Historial pipeline](docs/01-historial-pipeline.png)

### 2. Semgrep detectando SQL Injection
El análisis SAST encontró la vulnerabilidad en `src/app.py` línea 18.
Regla activada: `python.lang.security.audit.formatted-sql-query`

![SAST Semgrep](docs/02-semgrep-sql-injection.png)

### 3. Resumen final del pipeline
Los tres pasos de seguridad completados exitosamente.

![Resumen pipeline](docs/03-resumen-pipeline.png)

---

## Qué aprendimos construyendo este proyecto

### DevSecOps en una frase
> "Seguridad automatizada en cada paso del ciclo de desarrollo,
> sin frenar al equipo."

### El ciclo que vivimos
```
git push
   ↓
Pipeline se dispara automáticamente
   ↓
Secrets → Tests → SAST → SCA → Docker → Resumen
   ↓
Reporte: qué está mal, en qué archivo, en qué línea
   ↓
Desarrollador corrige
   ↓
git push → pipeline corre de nuevo → pasa limpio
```

### Las vulnerabilidades que pusimos a propósito

**Vulnerabilidad 1 — SQL Injection en `src/app.py`**

```python
# MAL: concatenar input del usuario en una query SQL
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

Semgrep lo detectó en la línea 18 con la regla
`python.lang.security.audit.formatted-sql-query`.

```python
# BIEN: parametros preparados
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

**Vulnerabilidad 2 — Dependencia vulnerable en `requirements.txt`**

```
Pillow==9.3.0  ← tiene CVEs conocidos
```

pip-audit la detecta comparando contra bases de datos de CVEs públicos.

### Lección importante que descubrimos
La primera versión del pipeline con Semgrep **no detectó** el SQL injection.
Tuvimos que agregar la regla `p/bandit` (específica para Python) para que
lo encontrara. Esto refleja la realidad de DevSecOps:

> Ninguna herramienta detecta el 100% de las vulnerabilidades.
> Por eso se usan múltiples capas de análisis.

---

## El pipeline — qué hace cada paso

| Paso | Herramienta | Qué detecta | Bloquea |
|------|-------------|-------------|---------|
| Secrets | Gitleaks | Contraseñas y API keys en el código | Sí |
| Tests | pytest | Funcionalidad rota y cobertura < 50% | Sí |
| SAST | Semgrep | Vulnerabilidades en el código fuente | No |
| SCA | pip-audit | Dependencias con CVEs conocidos | No |
| Docker | Trivy | Vulnerabilidades CRÍTICAS en la imagen | Sí |

---

## Estructura del proyecto
```
devsecops-demo/
├── .github/
│   └── workflows/
│       └── security.yml   ← pipeline principal
├── docs/                  ← evidencias del pipeline
├── src/
│   └── app.py             ← app con vulnerabilidad intencional
├── tests/
│   └── test_app.py        ← tests de seguridad con pytest
├── .gitleaks.toml         ← configuración de secrets scanning
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Ejercicio propuesto

1. Corrige el SQL injection en `src/app.py`
2. Actualiza `Pillow==9.3.0` a `Pillow>=10.3.0`
3. Haz push y verifica que el pipeline pase completamente limpio

Ese es el ciclo DevSecOps: **detectar → corregir → validar → repetir.**