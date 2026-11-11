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

### F-004 | 2026-11-11 | decision
Propongo pasar a un solo notebook para todo el proyecto, `notebooks/proyecto_regresion.ipynb`, trabajado por turnos. Motivo: entregamos un unico notebook coherente, y con turnos git nunca tiene que fusionar dos versiones del mismo `.ipynb`.
- Reglas del turno en `docs/TAREAS.md` ("Notebook unico y trabajo por turnos"). Mapa de secciones y normas del notebook en `docs/PLAN.md`.
- Tomo el primer turno con `T01`. No toques el notebook hasta que mi pull request este fusionado. Mientras tanto puedes avanzar `T04` en `app/`.
- Tu `T02` se integra como secciones 4 y 5. Solo quito tu carga de datos (ya esta en la seccion 1) y tu cabecera, y renumero las secciones; el analisis queda igual. Borro `notebooks/01b_eda_historial.ipynb` en el mismo pull request (sigue en el historial de git). Si no estas de acuerdo, dimelo al revisarlo.
- He cambiado la columna "Ficheros propios" de tus filas `T02` y `T06` para apuntar a sus secciones, y `T06` pasa a depender de `T05` porque comparten notebook. Revisalo en el pull request.
- Tu fila `T02` sigue en `en revision`, pero el pull request #1 ya esta fusionado: cuando puedas, pasala a `hecha`.

### F-005 | 2026-11-11 | aviso
Avance de `T01` en `docs/TAREAS.md` ("Avance de T01"). Resumen:
- Tu notebook ahora es `notebooks/proyecto_regresion.ipynb` (renombrado con `git mv`, mismo historial). Tu analisis esta intacto como secciones 4 y 5.
- Para tener todo igual: no hace falta que borres `01b_eda_historial.ipynb` a mano. Cuando el pull request de `T01` este fusionado, haz `git checkout main` y `git pull`, y git lo quita y trae el notebook nuevo. Antes, asegurate de no tener cambios sin guardar en tu notebook (`git status` limpio).
- Dos decisiones para `T03` que quiero hablar contigo: que hacemos con las 35 filas repetidas sin `ID`, y si usamos `SEX` como variable (puede ser discriminatorio). Detalle en las secciones 1 y 3 del notebook.

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


