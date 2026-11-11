# Plan de trabajo: Proyecto 7 Regresion

Plan tecnico del proyecto de Franco y Olena. Leer junto con `docs/TAREAS.md` (reparto, ramas y estado).

Regla general: avanzar fase a fase y no pasar a la siguiente sin cumplir el criterio de "hecho". Al cerrar cada fase, actualizar `docs/TAREAS.md`.

Las fases describen el contenido tecnico. Todo el proyecto va en un solo notebook, `notebooks/proyecto_regresion.ipynb`, que se trabaja por turnos (reglas en `docs/TAREAS.md`). Quien hace cada seccion esta en `docs/TAREAS.md`.

## Cifras de referencia (medidas el 2026-11-10)

Prueba rapida sin limpieza ni ajuste, split 80/20 con `random_state=42`, target `LIMIT_BAL` sin transformar. Sirven para saber si un resultado futuro es razonable.

| Caso de uso | Modelo | R2 train | R2 test | RMSE train | RMSE test | MAE test |
|---|---|---|---|---|---|---|
| Cliente nuevo (solo perfil) | Lineal | 0,092 | 0,079 | 123.606 | 124.579 | 99.475 |
| Cliente nuevo (solo perfil) | HistGradientBoosting | 0,210 | 0,177 | 115.326 | 117.746 | 91.724 |
| Revision (perfil + historial) | Lineal | 0,360 | 0,351 | 103.800 | 104.544 | 80.600 |
| Revision (perfil + historial) | HistGradientBoosting por defecto | 0,557 | 0,486 | 86.303 | 93.038 | 67.210 |
| Revision (perfil + historial) | Random Forest por defecto | 0,921 | 0,468 | 36.414 | 94.652 | 68.609 |
| Revision (perfil + historial) | Random Forest `min_samples_leaf=20` | 0,596 | 0,476 | 82.451 | 93.925 | 67.858 |

Conclusiones verificadas:
- El caso "cliente nuevo" tiene techo de R2 cercano a 0,18. El caso "revision" llega a 0,49. Por eso se recomienda "revision".
- Techo realista del proyecto: R2 de test alrededor de 0,50, RMSE alrededor de 93.000 NT$. Si aparece un R2 superior a 0,80, sospechar data leakage antes de celebrarlo.
- Transformar el target con logaritmo EMPEORA el R2 en todos los modelos (y rompe el lineal: R2 negativo). No aplicar log al target. Si aplicar log a las variables de importe.
- Anadir `default.payment.next.month` como variable sube el R2 solo 0,002. Se excluye: es informacion futura y no aporta.
- Random Forest por defecto memoriza (0,92 en train contra 0,47 en test). Ejemplo perfecto para ensenar overfitting.
- HistGradientBoosting por defecto tiene una diferencia de RMSE train/test del 7,8%. No cumple el limite del 5% sin regularizar.
- `LIMIT_BAL`: media 167.484, mediana 140.000, desviacion 129.748, minimo 10.000, maximo 1.000.000, asimetria 0,99.

## Decisiones

| Decision | Estado | Valor |
|---|---|---|
| Variable objetivo | Recomendada, falta confirmar con Olena | `LIMIT_BAL` |
| Caso de uso | Recomendado, falta confirmar con Olena | Revision de limite de cliente existente (perfil + historial de 6 meses) |
| Transformar target | Cerrada con datos | No |
| `default.payment.next.month` | Cerrada con datos | Se elimina de las variables |
| Definicion de overfitting | Propuesta, confirmar con el formador | Diferencia relativa de RMSE entre train y validacion menor al 5%. Informar tambien la de R2 |
| Dashboard | Abierta | Dentro de Streamlit (mas simple) o Power BI |

Formula de overfitting a usar: `(RMSE_validacion - RMSE_train) / RMSE_train * 100`.

Si Franco y Olena cambian el target o el caso de uso, actualizar esta tabla antes de seguir.

## Estructura de carpetas objetivo

```
data/UCI_Credit_Card.csv
notebooks/proyecto_regresion.ipynb   notebook unico del proyecto (por turnos)
src/preprocesamiento.py      funciones compartidas por el notebook y la app
models/modelo_final.joblib   pipeline entrenado
app/app.py                   Streamlit
docs/                        este plan y la guia
requirements.txt
README.md
.gitignore
```

## Secciones del notebook unico

El orden sigue la logica del problema: primero que queremos predecir, despues quien es el cliente, su historial, y por ultimo los modelos.

| Seccion | Contenido | Fase | Tarea |
|---|---|---|---|
| 0 | Introduccion: problema, caso de uso y dataset | 1 | T01 |
| 1 | Carga y calidad de los datos | 1 | T01 |
| 2 | Variable objetivo `LIMIT_BAL` | 1 | T01 |
| 3 | Perfil del cliente (`SEX`, `EDUCATION`, `MARRIAGE`, `AGE`) | 1 | T01 |
| 4 | Historial (`PAY_*`, `BILL_AMT*`, `PAY_AMT*`) | 1 | T02 |
| 5 | Correlaciones | 1 | T02 |
| 6 | Conclusiones del EDA | 1 | T01 |
| 7 | Limpieza y preprocesamiento | 2 | T03 |
| 8 | Modelo base | 3 | T03 |
| 9 | Ensembles: Random Forest y Gradient Boosting | 4 | T05 |
| 10 | Ensembles: XGBoost | 4 | T06 |
| 11 | Optuna y modelo final | 5 | T07 |
| 12 | Informe de metricas y conclusiones finales | 5 | T07 |

Normas del notebook:
- Una sola carga de datos (seccion 1) y un solo bloque de imports y estilo de graficos al principio. Motivo: si cada seccion recarga o reconfigura, el notebook final repite codigo y puede dar resultados distintos segun desde donde se ejecute.
- Nombres de variables con prefijo de su seccion cuando sean intermedios (por ejemplo `cols_pay`, `resumen_edu`). Motivo: en un notebook largo, reutilizar un nombre para otra cosa cambia resultados sin dar error.
- Cada seccion termina con una celda markdown de conclusiones. Motivo: la seccion siguiente parte de esas decisiones.
- Antes de cerrar un turno, "Restart & Run All" sin errores y con las salidas guardadas. Motivo: demuestra que el notebook corre de arriba abajo sin estado oculto, y la entrega necesita las salidas visibles.
- Las funciones que tambien use la app van en `src/`, no en el notebook. Motivo: la app no puede importar un notebook, y un `.py` se revisa bien en git.

## Fase 0: Preparacion del entorno

Objetivo: que el proyecto se pueda ejecutar y versionar.

Estado real de la maquina (verificado): Python 3.13.15, numpy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1, matplotlib 3.11.2, seaborn 0.13.2, streamlit 1.66.1, joblib 1.6.0, git 2.55.0. NO instalados: optuna, xgboost, jupyter/ipykernel, pytest. La carpeta no es repo git.

Pasos:
1. Usar un entorno virtual: cada proyecto con sus versiones, reproducible en las dos maquinas.
2. Crear el entorno: `python -m venv .venv` y activarlo con `.venv\Scripts\Activate.ps1`.
3. Instalar: numpy, pandas, scikit-learn, matplotlib, seaborn, streamlit, joblib, ipykernel, optuna, xgboost, pytest. Despues `pip freeze > requirements.txt`.
4. `git init`, `.gitignore` (`.venv/`, `__pycache__/`, `.ipynb_checkpoints/`), primer commit. Conectar el remoto de GitHub.
5. Tras instalar optuna y xgboost, comprobar su version y leer su documentacion antes de escribir codigo con ellos.

Hecho cuando: un notebook de prueba importa pandas y sklearn desde el kernel `.venv`.

## Fase 1: EDA (secciones 0 a 6)

Objetivo: entender los datos y justificar con graficos las decisiones de limpieza y de target.

Conceptos clave: target y features, tipos de variable (numerica, categorica, ordinal), distribucion y asimetria, outliers, correlacion (y que correlacion no es causalidad), multicolinealidad.

Pasos:
1. Carga, `shape`, `info`, `describe`, nulos y duplicados.
2. Target `LIMIT_BAL`: histograma y boxplot. Hacer notar que solo toma 81 valores (casi todos multiplos de 10.000; excepciones: 16.000 en 2 filas y 327.680 en 1) y la cola a la derecha.
3. Categoricas (`SEX`, `EDUCATION`, `MARRIAGE`): conteos y boxplot de `LIMIT_BAL` por categoria. Detectar los codigos no documentados.
4. `AGE`: distribucion y relacion con el limite.
5. `PAY_*`: conteos por valor y limite medio segun retraso.
6. `BILL_AMT*` y `PAY_AMT*`: histogramas en escala normal y logaritmica, para ver la asimetria.
7. Mapa de calor de correlaciones. Senalar el bloque `BILL_AMT1..6` (0,80 a 0,95) y las correlaciones con el target (maxima 0,30).
8. Celda final de conclusiones en markdown: lista de problemas y que se hara con cada uno.

Errores tipicos a vigilar: graficar sin titulo ni ejes, sacar conclusiones causales de una correlacion, querer borrar las facturas negativas (son saldo a favor, no errores).

Hecho cuando: Franco puede explicar con sus palabras por que se elige `LIMIT_BAL` y que tres problemas de calidad tiene el dataset.

## Fase 2: Limpieza y preprocesamiento (seccion 7)

Objetivo: dejar los datos listos sin contaminar la evaluacion.

Conceptos clave: data leakage, split train/test, por que el preprocesado se ajusta solo con train, Pipeline y ColumnTransformer, one-hot encoding, escalado, transformacion logaritmica.

Decisiones de limpieza:
- Eliminar `ID` (identificador, sin informacion).
- Eliminar `default.payment.next.month` (dato futuro, leakage).
- Renombrar `PAY_0` a `PAY_1` para que la numeracion coincida con `BILL_AMT1` y `PAY_AMT1`.
- `EDUCATION`: agrupar 0, 5 y 6 en 4 ("otros"). `MARRIAGE`: agrupar 0 en 3 ("otros").
- `SEX`, `EDUCATION`, `MARRIAGE`: one-hot para el modelo lineal. Los arboles no lo necesitan, pero se mantiene un unico pipeline por modelo.
- `PAY_*`: se dejan numericas (son ordinales). Interpretacion habitual, no oficial: -2 sin consumo, -1 pagado completo, 0 pago minimo, 1 a 8 meses de retraso.
- `BILL_AMT*`: log con signo, `sign(x) * log1p(abs(x))`, porque hay negativos. `PAY_AMT*`: `log1p`.
- Escalado (`StandardScaler`) solo para modelos lineales.

Variables nuevas permitidas (probar si mejoran, no asumirlo): media y maximo de factura, numero de meses con retraso, retraso maximo, ratio pago/factura, tendencia de la factura (mes 1 menos mes 6).

Variables PROHIBIDAS: cualquier cosa que use `LIMIT_BAL` (por ejemplo utilizacion = factura / limite). Contienen el target: es leakage directo.

Matiz honesto para el informe: la factura esta limitada por el limite de credito, asi que el historial "lleva dentro" parte del target. En el caso "revision" es legitimo (el banco ya conoce ese historial), pero hay que decirlo en las conclusiones.

Esquema de validacion:
- `train_test_split` 80/20, `random_state=42`. El test se guarda y se usa una sola vez, al final.
- Dentro del 80%: validacion cruzada de 5 folds para comparar modelos y medir overfitting.
- Todo el preprocesado dentro de un `Pipeline`, para que cada fold ajuste escalado y codificacion solo con sus datos de entrenamiento.

Nota tecnica: las funciones propias (log con signo, agrupacion de codigos) van en `src/preprocesamiento.py` y se usan con `FunctionTransformer`. No usar `lambda`: joblib no puede guardar lambdas y la app de Streamlit no podria cargar el modelo.

Nota pandas 3: la asignacion encadenada (`df[cond]["col"] = x`) no modifica el DataFrame. Usar siempre `df.loc[cond, "col"] = x`.

Hecho cuando: existe un pipeline de preprocesado que transforma train sin errores y Franco sabe explicar que es leakage con un ejemplo de este dataset.

## Fase 3: Modelo base (seccion 8)

Objetivo: tener una referencia simple contra la que comparar todo lo demas.

Conceptos clave: regresion lineal (coeficientes), MAE, RMSE, R2, por que hace falta un baseline, residuos.

Pasos:
1. Baseline tonto: `DummyRegressor` que predice siempre la media. Su R2 es 0. Todo modelo debe superarlo.
2. `LinearRegression` dentro del pipeline. Esperado: R2 cerca de 0,35 y RMSE cerca de 104.500.
3. Metricas en train y validacion (con `cross_validate` y `return_train_score=True`), y calculo del overfitting.
4. Probar `Ridge` y explicar regularizacion a nivel intuitivo.
5. Graficos: prediccion vs real, histograma de residuos, residuos vs prediccion.
6. Interpretar coeficientes (con variables escaladas, el tamano es comparable).

Funciones de scikit-learn 1.9.1 comprobadas en esta maquina: `root_mean_squared_error`, `mean_absolute_error`, `r2_score`, `TransformedTargetRegressor`, `HistGradientBoostingRegressor`, `RandomForestRegressor`.

Errores tipicos: evaluar sobre train y creer que es el rendimiento real, mirar el test en cada prueba, interpretar el R2 como "porcentaje de aciertos".

Hecho cuando: hay una tabla con Dummy, Lineal y Ridge (MAE, RMSE, R2, overfitting) y Franco interpreta el grafico de residuos.

## Fase 4: Ensembles y validacion cruzada (secciones 9 y 10)

Objetivo: mejorar al modelo base y cumplir overfitting menor al 5%.

Conceptos clave: arbol de decision, bagging (Random Forest), boosting (Gradient Boosting, XGBoost), sesgo y varianza, validacion cruzada, regularizacion de arboles, feature importance.

Pasos:
1. Un solo arbol sin limite de profundidad: R2 de train casi perfecto, validacion mala. Demostracion visual de overfitting.
2. Random Forest por defecto: mostrar 0,92 contra 0,47. Luego limitarlo (`min_samples_leaf`, `max_depth`, `max_features`) y ver como baja la diferencia.
3. Gradient Boosting (usar `HistGradientBoostingRegressor`, mucho mas rapido que `GradientBoostingRegressor` con 30.000 filas) y XGBoost.
4. Tabla comparativa de todos los modelos con validacion cruzada: media y desviacion de RMSE, MAE, R2 y overfitting.
5. Importancia de variables: la del modelo y `permutation_importance` (mas fiable). Comentar el efecto de la multicolinealidad de `BILL_AMT*`, que reparte la importancia entre columnas gemelas.

Aviso de tiempo: Random Forest con 100 arboles sobre este dataset tarda. La prueba de referencia completa supero los 2 minutos. Usar `n_jobs=-1` y pocos arboles mientras se explora.

Hecho cuando: hay un modelo candidato con R2 de validacion cerca de 0,48 y overfitting inferior al 5%, y Franco explica la diferencia entre bagging y boosting.

## Fase 5: Optuna y modelo final (secciones 11 y 12)

Objetivo: ajustar hiperparametros de forma sistematica y cerrar el modelo.

Conceptos clave: hiperparametro contra parametro, por que no se ajusta a mano ni con el test, busqueda bayesiana a nivel intuitivo, evaluacion final unica.

Pasos:
1. Definir la funcion objetivo: RMSE medio de validacion cruzada del pipeline completo.
2. Espacio de busqueda centrado en parametros que regulan la complejidad (profundidad, tamano minimo de hoja, tasa de aprendizaje, numero de arboles, regularizacion).
3. Guardar en cada prueba tambien el overfitting y elegir el mejor trial entre los que cumplen menos del 5%, no el de menor RMSE a secas.
4. Graficos de Optuna: historial de optimizacion e importancia de hiperparametros.
5. Reentrenar el mejor modelo con todo train, evaluar UNA vez en test y reportar.
6. Informe final: tabla de metricas, feature importance, residuos, prediccion vs real, conclusiones y limitaciones.
7. Guardar el pipeline completo con `joblib.dump` en `models/modelo_final.joblib`.

Esperar una mejora pequena (uno o dos puntos de R2). Explicarlo de antemano para que no se viva como fracaso: el techo lo ponen los datos, no el ajuste.

Hecho cuando: existe `models/modelo_final.joblib`, las metricas de test estan documentadas y el overfitting es menor al 5%.

## Fase 6: App Streamlit y dashboard

Objetivo: productivizar el modelo.

Contenido minimo:
1. Pagina de prediccion: formulario con las variables del cliente, boton y limite recomendado. Redondear la salida al multiplo de 10.000 mas cercano (los limites reales lo son) y mostrar el margen de error tipico (MAE).
2. Pagina de dashboard: graficos clave del EDA y metricas del modelo (o Power BI si lo prefieren).
3. Feedback (nivel medio): guardar en CSV cada prediccion con la opinion del usuario o el valor real, para reentrenar mas adelante.

Simplificar el formulario: 23 campos son demasiados. Opciones: valores por defecto con la mediana, o agrupar los seis meses en un bloque plegable.

La app debe importar `src/preprocesamiento.py` igual que el notebook, o joblib no podra cargar el modelo.

Hecho cuando: `streamlit run app/app.py` arranca, predice y guarda feedback.

## Fase 7: Extras (solo si sobra tiempo)

Orden recomendado por relacion esfuerzo/valor:
1. Tests unitarios con pytest de las funciones de `src/preprocesamiento.py`.
2. Despliegue en Streamlit Community Cloud.
3. SQLite en lugar de CSV para el feedback.
4. Dockerfile.
5. MLOps (data drift, A/B testing): solo descripcion conceptual en el README salvo que haya tiempo real.

## Reparto sugerido de la semana

| Dia | Trabajo |
|---|---|
| 1 | Fase 0 y Fase 1 |
| 2 | Fase 2 y Fase 3 |
| 3 | Fase 4 |
| 4 | Fase 5 |
| 5 | Fase 6 |
| 6 | README, repaso de la presentacion, extras |
| 7 | Margen |
