# Observaciones

Mensajes entre Franco y Olena. Sirve para decisiones, avisos de cambios en ficheros compartidos, dudas y bloqueos.

Reglas:
- Cada persona escribe solo en su seccion, anadiendo al final de ella. Asi git fusiona sin conflictos.
- No se editan ni se borran entradas antiguas. Para responder, se escribe una entrada nueva en la seccion propia citando el identificador.
- Formato: `### F-003 | 2026-11-12 | tipo` y debajo el texto. Franco usa `F-`, Olena usa `O-`.
- Tipos: `aviso`, `decision`, `duda`, `bloqueo`, `respuesta`.
- Se lee al empezar a trabajar y se escribe al terminar.

## Seccion de Franco

### F-001 | 2026-11-10 | aviso
Repo preparado. Antes de empezar lee `docs/PLAN.md` (plan tecnico y cifras medidas) y `docs/TAREAS.md` (reparto y ramas).

### F-002 | 2026-11-10 | decision
Necesito tu confirmacion en tres puntos:
1. Target `LIMIT_BAL` con el caso de uso "revision de limite de cliente existente". Motivo: R2 de test 0,49 frente a 0,18 en el caso "cliente nuevo". Detalle en `docs/PLAN.md`.
2. El reparto de `docs/TAREAS.md`. Si quieres cambiar alguna tarea, dimelo aqui.
3. Dashboard dentro de Streamlit o en Power BI.

### F-003 | 2026-11-11 | aviso
Gracias por `O-001` y `O-002`: decisiones confirmadas (target `LIMIT_BAL`, reparto, dashboard en Streamlit) y hallazgos de `T02` anotados para `T03`.
Cambios en ficheros compartidos:
- `requirements.txt` ahora tiene las versiones fijadas (numpy 2.5.4, pandas 3.1.1, scikit-learn 1.9.1, matplotlib 3.11.2, seaborn 0.13.2, streamlit 1.67.0, joblib 1.6.0, ipykernel 7.4.0, optuna 5.0.0, xgboost 3.4.1, pytest 9.2.0). Instala con `pip install -r requirements.txt` en un `.venv` propio.
- El repo se renombro a `ML_project_UCI_Credit_Card_data`. Actualiza tu remoto: `git remote set-url origin https://github.com/Bootcamp-DA-P3/ML_project_UCI_Credit_Card_data.git`.
- `T00` queda `hecha`. Empiezo `T01` en `franco/eda-perfil`.

## Seccion de Olena

### O-001 | 2026-11-10 | respuesta
En respuesta a `F-002`:
1. Confirmo el target `LIMIT_BAL` con el caso de uso "revision de limite de cliente existente" (perfil + historial de 6 meses).
2. Confirmo el reparto de tareas propuesto en `docs/TAREAS.md`.
3. Prefiero integrar el dashboard analitico dentro de Streamlit.
Empiezo con `T02` en la rama `olena/eda-historial`.

### O-002 | 2026-11-11 | aviso
Terminado `T02` en `notebooks/01b_eda_historial.ipynb` (rama `olena/eda-historial`). Hallazgos confirmados para `T03` (`src/preprocesamiento.py`):
- `PAY_0` corresponde a septiembre (mes 1) y salta a `PAY_2`: renombrar `PAY_0` -> `PAY_1` y mantener `PAY_*` como numericas ordinales (correlacion de `-0,24` a `-0,30` con `LIMIT_BAL`).
- `BILL_AMT1..6` tienen entre 590 y 688 valores negativos por mes (saldo a favor, conservar filas) y asimetria `2,7 - 3,1`: aplicar log con signo `sign(x) * log1p(abs(x))`.
- `PAY_AMT1..6` no tienen negativos y presentan fuerte asimetria (`10,6 - 30,5`): aplicar `log1p(x)`.
- Alta multicolinealidad entre `BILL_AMT1..6` (`0,80` a `0,95`) y correlacion lineal maxima de `0,30` con `LIMIT_BAL`.


