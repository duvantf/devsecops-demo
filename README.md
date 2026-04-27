# DevSecOps Demo — Python

Proyecto de aprendizaje práctico de DevSecOps.
El pipeline detecta vulnerabilidades automáticamente en cada `git push`.

## Qué hace el pipeline

| Paso | Herramienta | Qué detecta |
|------|-------------|-------------|
| SAST | Semgrep | SQL injection y vulnerabilidades en código |
| SCA  | pip-audit | Dependencias con CVEs conocidos |
| Docker | Trivy | Vulnerabilidades en la imagen del contenedor |

## Vulnerabilidades intencionales incluidas

Este proyecto tiene dos problemas a propósito para que los veas en acción:

1. **SQL Injection** en `src/app.py` — Semgrep lo detecta
2. **Pillow 9.1.0** en `requirements.txt` — pip-audit reporta CVE-2022-22817

## Cómo usarlo

### 1. Clonar y configurar
```bash
git clone https://github.com/TU_USUARIO/devsecops-demo.git
cd devsecops-demo
```

### 2. Hacer push y ver el pipeline
```bash
git add .
git commit -m "feat: primer commit con pipeline DevSecOps"
git push origin main
```

### 3. Ver los resultados
- Ve a tu repositorio en GitHub
- Haz clic en la pestaña **Actions**
- Abre el workflow "Pipeline DevSecOps"
- Revisa los reportes de cada paso

### 4. Corregir las vulnerabilidades (ejercicio)
Intenta arreglar los problemas y vuelve a hacer push:
- Cambia la query SQL en `src/app.py` por la versión segura
- Actualiza `Pillow==9.1.0` a `Pillow>=9.1.1` en `requirements.txt`

## Estructura del proyecto
```
devsecops-demo/
├── .github/
│   └── workflows/
│       └── security.yml   ← pipeline principal
├── src/
│   └── app.py             ← app con vulnerabilidad intencional
├── Dockerfile
├── requirements.txt       ← dependencia vulnerable intencional
└── README.md
```
