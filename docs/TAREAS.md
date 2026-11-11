# Tareas

Reparto propuesto el 2026-11-10 por Franco. Olena debe revisarlo y aceptarlo o proponer cambios en `OBSERVACIONES.md`.

Reglas:
- Cada persona edita solo sus filas.
- Estados: `pendiente`, `en curso`, `en revision` (pull request abierto), `hecha` (fusionada en `main`), `bloqueada`.
- No empezar una tarea hasta que sus dependencias esten en `hecha`.
- La rama se crea desde `main` actualizado: `git checkout main`, `git pull`, `git checkout -b nombre/descripcion`.

## Notebook unico y trabajo por turnos (acordado el 2026-11-11)

Todo el proyecto se entrega en un solo notebook: `notebooks/proyecto_regresion.ipynb`. El mapa de secciones esta en `docs/PLAN.md`.

Reglas del turno:
1. Solo una persona tiene el turno del notebook a la vez: la que tiene su tarea de notebook `en curso`. Motivo: un `.ipynb` es un JSON con salidas y git no sabe fusionar dos versiones cambiadas a la vez. El turno evita el conflicto en vez de tener que arreglarlo.
2. Para tomar el turno: comprobar en esta tabla que ninguna otra tarea de notebook esta `en curso` o `en revision`, poner la propia `en curso`, y escribir un `aviso` en `OBSERVACIONES.md`. Motivo: la otra persona sabe que no debe tocar el notebook.
3. Al empezar el turno: `git checkout main`, `git pull` y rama nueva. Motivo: se parte de la ultima version, con el trabajo de la otra persona incluido.
4. Cada uno escribe solo sus secciones. Si hace falta cambiar una seccion de la otra persona, se pide en `OBSERVACIONES.md`, o se hace y se explica en el pull request para que la duena lo apruebe. Motivo: quien escribio la seccion es quien sabe por que esta asi.
5. Al terminar el turno: "Restart & Run All" sin errores, commit, pull request y revision de la otra persona. El turno se libera cuando el pull request esta fusionado en `main`. Motivo: si alguien empieza antes del merge, parte de una version vieja y vuelve el conflicto.
6. Mientras una persona tiene el turno, la otra trabaja en ficheros que no son el notebook (`app/`, `src/` si es su dueno, README, presentacion) o revisa. Motivo: no hay esperas sin hacer nada.

## Tabla

| ID | Tarea | Responsable | Rama | Ficheros propios | Depende de | Estado |
|---|---|---|---|---|---|---|
| T00 | Entorno, estructura del repo y primer commit | Franco | `main` (solo esta vez) | `requirements.txt`, `.gitignore`, `README.md` | | hecha |
| T01 | EDA A: target y perfil (`LIMIT_BAL`, `SEX`, `EDUCATION`, `MARRIAGE`, `AGE`), crear el notebook unico e integrar en el las secciones de T02 | Franco | `franco/eda-perfil` | notebook unico, secciones 0 a 3 y 6 | T00 | en revision |
| T02 | EDA B: historial (`PAY_*`, `BILL_AMT*`, `PAY_AMT*`) y correlaciones | Olena | `olena/eda-historial` | notebook unico, secciones 4 y 5 (hecho en `notebooks/01b_eda_historial.ipynb`, se integra en T01) | T00 | en revision |
| T03 | Limpieza, preprocesamiento y modelo base | Franco | `franco/preprocesamiento-base` | notebook unico, secciones 7 y 8; `src/preprocesamiento.py` | T01, T02 | pendiente |
| T04 | Esqueleto de la app y dashboard con graficos del EDA | Olena | `olena/app-esqueleto` | `app/` | T01, T02 | pendiente |
| T05 | Ensembles A: Random Forest y Gradient Boosting con validacion cruzada | Franco | `franco/ensembles-rf-gb` | notebook unico, seccion 9 | T03 | pendiente |
| T06 | Ensembles B: XGBoost con validacion cruzada | Olena | `olena/ensembles-xgboost` | notebook unico, seccion 10 | T05 | pendiente |
| T07 | Optuna, modelo final e informe de metricas | Franco | `franco/optuna-modelo-final` | notebook unico, secciones 11 y 12; `models/modelo_final.joblib` | T05, T06 | pendiente |
| T08 | App: prediccion con el modelo final y recogida de feedback | Olena | `olena/app-modelo-feedback` | `app/` | T04, T07 | pendiente |
| T09 | README final | Franco | `franco/readme-final` | `README.md` | T07, T08 | pendiente |
| T10 | Presentacion | Olena | `olena/presentacion` | `docs/presentacion/` | T07, T08 | pendiente |

## Orden de turnos y trabajo en paralelo

- Turnos del notebook: T01 -> T03 -> T05 -> T06 -> T07. T06 pasa a depender de T05 porque comparten notebook.
- T02 ya se hizo en un notebook aparte antes de este acuerdo. T01 integra sus celdas como secciones 4 y 5 y borra `notebooks/01b_eda_historial.ipynb` (queda en el historial de git). Olena lo aprueba al revisar el pull request de T01.
- En paralelo con el turno del notebook: T04 (app) durante T01 y T03; T08 (app) durante T07; T09 y T10 a la vez al final.
- T05 y T06 usan el mismo pipeline de `src/preprocesamiento.py` y el mismo split (`random_state=42`) para que los resultados sean comparables.
- T07 necesita las tablas de resultados de T05 y T06.

## Duenos de ficheros compartidos

| Fichero | Dueno | Como se cambia |
|---|---|---|
| `notebooks/proyecto_regresion.ipynb` | Por turnos (cada seccion, su autor) | Solo quien tiene el turno, segun las reglas de arriba |
| `docs/PLAN.md` | Franco | Aviso en `OBSERVACIONES.md` y pull request |
| `src/preprocesamiento.py` | Franco | Olena pide cambios en `OBSERVACIONES.md` |
| `requirements.txt` | Franco | Quien necesite una libreria nueva lo avisa en `OBSERVACIONES.md` |
| `app/` | Olena | Franco pide cambios en `OBSERVACIONES.md` |
| `docs/TAREAS.md` | Los dos | Cada uno solo sus filas |
| `OBSERVACIONES.md` | Los dos | Cada uno solo su seccion |

## Avance de T01 (2026-11-11)

Hecho en la rama `franco/eda-perfil`:
- `notebooks/01b_eda_historial.ipynb` renombrado con `git mv` a `notebooks/proyecto_regresion.ipynb` (conserva el historial de git). Es el notebook unico del proyecto.
- Secciones nuevas: 0 (introduccion, caso de uso y por que `LIMIT_BAL`), 1 (carga y calidad: unica carga de datos, `info`, `describe`, duplicados), 2 (target `LIMIT_BAL`), 3 (perfil: `SEX`, `EDUCATION`, `MARRIAGE`, `AGE`) y 6 (tabla de problemas del EDA y acciones para la seccion 7).
- Celdas de T02 conservadas con sus salidas como secciones 4.1, 4.2 y 5. Solo cambia la numeracion y `cols_historial` pasa al inicio de la seccion 4.
- Las 30 celdas se ejecutan de principio a fin sin errores.
- Hallazgos nuevos: 35 filas repetidas si se quita `ID` (la mayoria, cuentas sin actividad); la edad tiene relacion en U invertida con el limite (mediana 50.000 entre 21 y 25 anos, 180.000 entre 30 y 40, 110.000 entre 50 y 60); `LIMIT_BAL` tiene 3 filas que no son multiplo de 10.000.
- Decisiones abiertas para T03, a acordar entre los dos: que hacer con los 35 duplicados y si se usa `SEX` como variable.
- Docs actualizados con el metodo de notebook unico por turnos: este fichero, `docs/PLAN.md` y `OBSERVACIONES.md` (`F-004`).

Notebook ejecutado completo y guardado con salidas. Pull request abierto: falta la revision de Olena y el merge.

## Notas de T00 (maquina de Franco, 2026-11-10)

- Python 3.13.15. Instalado en el Python global: numpy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1, matplotlib 3.11.2, seaborn 0.13.2, streamlit 1.66.1, joblib 1.6.0.
- Falta: crear `.venv`, instalar optuna, xgboost, ipykernel y pytest, fijar versiones con `pip freeze`, primer commit y conectar el remoto de GitHub.
