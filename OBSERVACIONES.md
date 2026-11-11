# Observaciones

Mensajes entre Franco y Olena. Sirve para decisiones, avisos de cambios en ficheros compartidos, dudas y bloqueos.

Reglas:
- Cada persona escribe solo en su seccion, anadiendo al final de ella. Asi git fusiona sin conflictos.
- No se editan ni se borran entradas antiguas. Para responder, se escribe una entrada nueva en la seccion propia citando el identificador.
- Formato: `### F-003 | 2026-11-12 | tipo` y debajo el texto. Franco usa `F-`, Olena usa `O-`.
- Tipos: `aviso`, `decision`, `duda`, `bloqueo`, `respuesta`, `traspaso`.
- Se lee al empezar a trabajar y se escribe al terminar.
- `traspaso`: se escribe al cerrar un turno del notebook, con esta plantilla:

```
### F-00X | fecha | traspaso
Tarea y rama: ...
Pull request: #...
Hecho: secciones y ficheros que se tocaron, en pocas lineas.
Decisiones nuevas: ...
Cambios en secciones o ficheros de la otra persona: ...
Que tiene que revisar la otra persona: ...
Que le toca a la otra persona y por donde empezar: ...
Siguiente turno del notebook: quien y con que tarea.
```

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

### F-006 | 2026-11-11 | aviso
En respuesta a `O-003`, y toma del turno del notebook:
- **Tomo el turno con `T03`** en la rama `franco/preprocesamiento-base` (secciones 7 y 8, y `src/preprocesamiento.py`). No toques `notebooks/proyecto_regresion.ipynb` hasta que este pull request este fusionado. Mientras tanto puedes avanzar `T04` en `app/`.
- **Duplicados:** de acuerdo, los eliminamos antes del `train_test_split`. Un matiz: las 35 se contaron quitando solo `ID`. Con tu mismo argumento (que el modelo no vea la misma fila en train y test), lo que cuenta son las columnas que vera el modelo: sin `ID`, sin `default.payment.next.month` y sin `SEX` salen **93** filas repetidas (0,31%). Las busco con ese criterio en la seccion 7.2. Si no estas de acuerdo, dimelo al revisar el pull request.
- **`SEX`:** de acuerdo, la excluimos. En la seccion 7 medire el R2 con y sin `SEX` para dejar la decision justificada con datos.
- **Autoria en el notebook:** cada titulo de seccion termina ahora con la inicial de quien la hizo, `[F]` o `[L]`, y el indice de la seccion 0 tambien. He anadido `[L]` al titulo de tus secciones 4 y 5 (solo el titulo, el contenido no cambia) y `[L]` a la seccion 10 en el indice. La norma queda en `docs/PLAN.md` ("Normas del notebook"). Si prefieres otra letra o formato, dimelo.
- **Logaritmo en los importes: lo quitamos (cambia tu recomendacion de `O-002`).** En la seccion 8.2 medimos el modelo lineal con y sin logaritmo en `BILL_AMT*` y `PAY_AMT*`: R2 de validacion 0,364 sin logaritmo y 0,241 con logaritmo. La factura esta limitada por el limite de credito, asi que su relacion con `LIMIT_BAL` es casi una recta en escala original, y el logaritmo la curva. Para arboles da igual (no cambia el orden de los valores). `crear_preprocesador()` ya no aplica logaritmo por defecto; queda como opcion `usar_log=True`. Para `T06` (XGBoost) usa `crear_preprocesador()` sin parametros, igual que en `T05`.
- **`SEX` medido (seccion 8.3):** R2 de validacion 0,364 con y sin `SEX`. No aporta, asi que excluirla no cuesta precision.
- **Solo cifras calculadas en el notebook (norma nueva):** quito del texto los numeros que venian de la prueba previa y no de una celda del notebook (R2 0,49 y 0,18 en la introduccion, techo 0,50 y umbral 0,80 en la seccion 6, prueba con logaritmo en la seccion 2). En tu conclusion de las secciones 4 y 5 quite solo "(~0,35)" del punto 6; el resto queda igual. La norma esta en `docs/PLAN.md`.
- **Texto del notebook breve (norma nueva):** he recortado las celdas markdown de mis secciones (0 a 3, 6 y 7) a titulo, subtitulo y conclusiones con las palabras justas, sin parrafos explicativos. Tus secciones 4 y 5 no las he tocado; si quieres, recorta sus parrafos de introduccion en tu turno de T06 con el mismo criterio.
- **Traspaso de turno (nuevo):** al cerrar cada turno del notebook escribimos una entrada `traspaso` con la plantilla que hay al principio de este fichero, y actualizamos la tabla "Turno actual" de `docs/TAREAS.md` (regla 7). Asi, despues del `git pull`, cada uno sabe que se hizo y que le toca.
- Cambios en ficheros compartidos (al tomar el turno): `T01` pasa a `hecha` y `T03` a `en curso` en `docs/TAREAS.md`. En `docs/PLAN.md` (tabla "Decisiones") cierro target y caso de uso (`O-001`) y anado las dos decisiones de `O-003`.

### F-007 | 2026-11-11 | traspaso
Tarea y rama: `T03`, `franco/preprocesamiento-base`.
Pull request: #5.
Hecho:
- Seccion 7: limpieza fija, 93 filas repetidas eliminadas (quedan 29.907), split 80/20 (23.925 train, 5.982 test), comprobacion de funciones y pipeline de preprocesamiento (26 columnas).
- Seccion 8: validacion cruzada de 5 folds con la funcion `evaluar`. Modelo lineal: R2 de validacion 0,364, RMSE 104.144, MAE 79.937, overfitting 0,25%. Residuos y coeficientes.
- `src/preprocesamiento.py`: `agrupar_codigos`, `log_con_signo` y `crear_preprocesador(incluir_sex=False, usar_log=False)`.
- Notebook ejecutado de principio a fin sin errores y guardado con salidas.
Decisiones nuevas (detalle en `F-006` y en la tabla "Decisiones" de `docs/PLAN.md`):
- Duplicados buscados en las columnas del modelo: 93 filas, no 35.
- Sin logaritmo en los importes: empeora el modelo lineal (0,241 frente a 0,364).
- `SEX` fuera: no aporta (0,364 con y sin ella).
- Normas nuevas del notebook: inicial `[F]`/`[L]` en cada titulo, solo cifras calculadas en el notebook, texto breve sin parrafos explicativos.
Cambios en secciones o ficheros de la otra persona:
- Secciones 4 y 5: anadido `[L]` al titulo y quitado "(~0,35)" del punto 6 de las conclusiones. Nada mas.
Que tiene que revisar la otra persona:
- Secciones 7 y 8 del notebook y `src/preprocesamiento.py`.
- Que estes de acuerdo con quitar el logaritmo (era tu recomendacion de `O-002`) y con las 93 filas repetidas.
Que le toca a la otra persona y por donde empezar:
1. Revisar el pull request de `T03` y fusionarlo si esta bien. Despues, `git checkout main` y `git pull`.
2. Seguir con `T04` en `app/`. No tocar el notebook.
3. Para `T06` (cuando termine `T05`): usar `crear_preprocesador()` sin parametros y la funcion `evaluar` de la seccion 8 con el mismo `cv`, para que los resultados se puedan comparar con la tabla de la seccion 8.
Siguiente turno del notebook: Franco con `T05` (seccion 9), despues del merge.

### F-008 | 2026-11-11 | decision
Propuesta de cambio en el reparto: me gustaria hacer yo la app de Streamlit (`T04` y `T08`, carpeta `app/`).
- Si ya tienes algo avanzado de `T04`, dimelo y vemos como seguir sin perder tu trabajo.
- A cambio, propongo que te quedes con `T09` (README final), ademas de `T10` (presentacion). Si prefieres otra tarea, dimelo.
- No cambio las filas de `docs/TAREAS.md` hasta que respondas. Contestame con una entrada `O-` y, si estas de acuerdo, actualizamos el reparto.

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

### O-003 | 2026-11-11 | respuesta
En respuesta a `F-004` y `F-005`:
1. **Notebook unico y turnos:** De acuerdo con trabajar en `notebooks/proyecto_regresion.ipynb` por turnos, con la integracion de `T02` como secciones 4 y 5, y con que `T06` dependa de `T05`. He revisado `T01` (secciones 0 a 3 y 6) y paso `T02` a `hecha` en `docs/TAREAS.md`.
2. **35 filas duplicadas sin `ID`:** Propongo **eliminarlas** antes del `train_test_split` en `T03`. Motivo: aunque probablemente sean clientes distintos con cuentas sin actividad, si una copia cae en `train` y su gemela exacta en `test`, estariamos evaluando el modelo con observaciones identicas a las de entrenamiento (fuga de informacion entre train y test). Al ser solo 35 filas de 30.000 (`0,11%`), eliminarlas no afecta la distribucion estadistica y asegura un `test` limpio.
3. **Variable `SEX`:** Prefiero **excluirla** del modelo, comprobando en `T03` que el $R^2$ apenas varia al quitarla. Motivo: en concesion de credito real usar el sexo es discriminatorio y contrario a criterios eticos y regulatorios de banca responsable; ademas, si no aporta senal predictiva relevante frente al historial y resto del perfil, quitarla hace el modelo mas justo y simplifica el formulario de la app.


