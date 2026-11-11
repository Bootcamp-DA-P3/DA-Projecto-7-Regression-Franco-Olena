# Tareas

Reparto propuesto el 2026-11-10 por Franco (con su asistente). Olena debe revisarlo y aceptarlo o proponer cambios en `OBSERVACIONES.md`.

Reglas:
- Cada persona edita solo sus filas.
- Estados: `pendiente`, `en curso`, `en revision` (pull request abierto), `hecha` (fusionada en `main`), `bloqueada`.
- No empezar una tarea hasta que sus dependencias esten en `hecha`.
- La rama se crea desde `main` actualizado: `git checkout main`, `git pull`, `git checkout -b nombre/descripcion`.

## Tabla

| ID | Tarea | Responsable | Rama | Ficheros propios | Depende de | Estado |
|---|---|---|---|---|---|---|
| T00 | Entorno, estructura del repo y primer commit | Franco | `main` (solo esta vez) | `requirements.txt`, `.gitignore`, `README.md` | | en curso |
| T01 | EDA A: target y perfil (`LIMIT_BAL`, `SEX`, `EDUCATION`, `MARRIAGE`, `AGE`) | Franco | `franco/eda-perfil` | `notebooks/01a_eda_perfil.ipynb` | T00 | pendiente |
| T02 | EDA B: historial (`PAY_*`, `BILL_AMT*`, `PAY_AMT*`) y correlaciones | Olena | `olena/eda-historial` | `notebooks/01b_eda_historial.ipynb` | T00 | en curso |
| T03 | Limpieza, preprocesamiento y modelo base | Franco | `franco/preprocesamiento-base` | `notebooks/02_preprocesamiento_y_modelo_base.ipynb`, `src/preprocesamiento.py` | T01, T02 | pendiente |
| T04 | Esqueleto de la app y dashboard con graficos del EDA | Olena | `olena/app-esqueleto` | `app/` | T01, T02 | pendiente |
| T05 | Ensembles A: Random Forest y Gradient Boosting con validacion cruzada | Franco | `franco/ensembles-rf-gb` | `notebooks/03a_ensembles_rf_gb.ipynb` | T03 | pendiente |
| T06 | Ensembles B: XGBoost con validacion cruzada | Olena | `olena/ensembles-xgboost` | `notebooks/03b_ensembles_xgboost.ipynb` | T03 | pendiente |
| T07 | Optuna, modelo final e informe de metricas | Franco | `franco/optuna-modelo-final` | `notebooks/04_optuna_y_modelo_final.ipynb`, `models/modelo_final.joblib` | T05, T06 | pendiente |
| T08 | App: prediccion con el modelo final y recogida de feedback | Olena | `olena/app-modelo-feedback` | `app/` | T04, T07 | pendiente |
| T09 | README final | Franco | `franco/readme-final` | `README.md` | T07, T08 | pendiente |
| T10 | Presentacion | Olena | `olena/presentacion` | `docs/presentacion/` | T07, T08 | pendiente |

## Trabajo en paralelo

- T01 y T02 a la vez (dia 1).
- T03 y T04 a la vez (dia 2).
- T05 y T06 a la vez (dia 3). Los dos notebooks usan el mismo pipeline de `src/preprocesamiento.py` y el mismo split (`random_state=42`) para que los resultados sean comparables.
- T07 necesita las tablas de resultados de T05 y T06.
- T09 y T10 a la vez.

## Duenos de ficheros compartidos

| Fichero | Dueno | Como se cambia |
|---|---|---|
| `AGENTS.md`, `docs/PLAN.md`, `docs/GUIA_PROFESOR.md` | Franco | Aviso en `OBSERVACIONES.md` y pull request |
| `src/preprocesamiento.py` | Franco | Olena pide cambios en `OBSERVACIONES.md` |
| `requirements.txt` | Franco | Quien necesite una libreria nueva lo avisa en `OBSERVACIONES.md` |
| `app/` | Olena | Franco pide cambios en `OBSERVACIONES.md` |
| `docs/TAREAS.md` | Los dos | Cada uno solo sus filas |
| `OBSERVACIONES.md` | Los dos | Cada uno solo su seccion |

## Notas de T00 (maquina de Franco, 2026-11-10)

- Python 3.13.15. Instalado en el Python global: numpy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1, matplotlib 3.11.2, seaborn 0.13.2, streamlit 1.66.1, joblib 1.6.0.
- Falta: crear `.venv`, instalar optuna, xgboost, ipykernel y pytest, fijar versiones con `pip freeze`, primer commit y conectar el remoto de GitHub.
