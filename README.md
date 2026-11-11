# Proyecto 7: Regresion sobre limite de credito

Proyecto grupal del bootcamp de Data Analytics de Factoria F5 Madrid. Autores: Franco y Olena.

Objetivo: predecir el limite de credito (`LIMIT_BAL`) de clientes de tarjeta a partir de su perfil y de su historial de pagos de seis meses, con el dataset "Default of Credit Card Clients" (UCI).

Estado: en desarrollo. Este README se completara al final con resultados y capturas.

## Instalacion

```powershell
git clone <URL del repo>
cd <carpeta del repo>
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Estructura

```
data/        dataset original
notebooks/   EDA, preprocesamiento, modelos y optimizacion
src/         funciones compartidas por notebooks y app
models/      modelo entrenado
app/         aplicacion Streamlit
docs/        plan, guia y reparto de tareas
```

## Como trabajamos

Cada persona trabaja en su propia rama y los cambios entran en `main` por pull request. El plan tecnico esta en `docs/PLAN.md`, el reparto en `docs/TAREAS.md` y las notas de equipo en `OBSERVACIONES.md`.
