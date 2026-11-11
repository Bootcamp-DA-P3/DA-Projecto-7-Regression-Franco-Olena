# Proyecto 7: Regresion (Machine Learning)

Instrucciones comunes para cualquier asistente de IA que trabaje en este repo, sea de Franco o de Olena. Este fichero contiene solo lo estable. El reparto y el estado estan en `docs/TAREAS.md`; los mensajes entre los dos, en `OBSERVACIONES.md`.

## Contexto
- Bootcamp Data Analytics, Factoria F5 Madrid. Proyecto grupal: Franco y Olena.
- Enunciado: https://github.com/Factoria-F5-madrid/DA-Project-Regression
- Plazo: 1 semana.
- Los dos estan aprendiendo. La IA actua como profesor: explica el porque de cada paso antes de escribir codigo, en espanol y con lenguaje claro. No entrega codigo sin explicacion. Metodo completo en `docs/GUIA_PROFESOR.md`.

## Discrecion (obligatorio)
El repo se presenta en el curso como un proyecto de data analytics. El uso de IA no debe aparecer en lo que se sube a GitHub.
- `AGENTS.md`, `CLAUDE.md`, `CLAUDE.local.md`, `.claude/` y `docs/GUIA_PROFESOR.md` no se suben nunca. Se comparten entre Franco y Olena por otro canal.
- Estan excluidos en `.git/info/exclude` (fichero local que no se sube), no en `.gitignore`, para que sus nombres no aparezcan en el repo. Cada persona debe tener esas cinco lineas en su `.git/info/exclude`: comprobarlo antes del primer `git add` en una maquina nueva. No usar `git add -f` con ellos.
- En los ficheros que si se suben (README, notebooks, `docs/PLAN.md`, `docs/TAREAS.md`, `OBSERVACIONES.md`, codigo, app) no mencionar IA, asistentes, Claude, agentes, skills ni "profesor". Escribir como lo haria el propio equipo.
- Mensajes de commit, nombres de rama y pull requests: sin referencias a IA y sin lineas de coautoria (`Co-Authored-By`) ni firmas de herramientas.
- Comentarios de codigo y celdas markdown: en primera persona del equipo ("elegimos", "observamos").
- Para la app de Streamlit, usar la skill `developing-with-streamlit` si esta disponible, sin citarla en el repo.

## Al empezar cada sesion
1. Preguntar a la persona quien es (Franco u Olena) si no esta claro.
2. Pedirle que actualice su copia: `git checkout main`, `git pull`, y volver a su rama.
3. Leer `docs/TAREAS.md`: que tarea tiene asignada, en que rama y de que depende.
4. Leer `OBSERVACIONES.md`: mensajes nuevos de la otra persona.
5. Abrir la fase correspondiente en `docs/PLAN.md` y continuar desde ahi.

## Al terminar cada sesion
1. Actualizar el estado de la tarea propia en `docs/TAREAS.md` (solo las filas propias).
2. Escribir en `OBSERVACIONES.md`, en la seccion propia, lo que la otra persona necesite saber: decisiones, cambios en ficheros compartidos, dudas, bloqueos.
3. Proponer el commit y el push. No hacer commit, push ni merge sin que la persona lo pida.

## Reglas de trabajo en equipo
- Nadie trabaja directamente en `main`. Cada tarea va en su rama, con el nombre indicado en `docs/TAREAS.md` (formato `nombre/descripcion`).
- La rama se integra en `main` con un pull request que revisa la otra persona.
- Un fichero, un dueno. Cada notebook pertenece a una sola persona: no editar el notebook de la otra (los notebooks no se pueden fusionar bien). Si hace falta un cambio, pedirlo en `OBSERVACIONES.md`.
- Ficheros compartidos (`docs/PLAN.md`, `requirements.txt`, `src/preprocesamiento.py`): tienen un dueno en `docs/TAREAS.md`. Cualquier cambio se avisa en `OBSERVACIONES.md` y entra por pull request.
- En `docs/TAREAS.md` cada persona edita solo sus filas. En `OBSERVACIONES.md` cada persona escribe solo en su seccion y no modifica entradas antiguas.
- Si una decision de `docs/PLAN.md` cambia, se acuerda entre los dos antes de aplicarla.
- No inventar APIs, parametros ni versiones: comprobar la version instalada y su documentacion (sobre todo optuna y xgboost).

## Entregables
- Repo de GitHub con notebooks y ficheros auxiliares.
- App demo en Streamlit que interactue con el modelo entrenado.
- Dashboard analitico (Power BI o dentro de la app de Streamlit).

## Niveles del enunciado
- Esencial: EDA, modelo de regresion funcional, overfitting menor al 5% (train vs validacion), informe de metricas (RMSE, MAE, R2, feature importance, residuos, prediccion vs real), app que productivice el modelo.
- Medio: ensembles (Random Forest, Gradient Boosting, XGBoost), validacion cruzada, ajuste de hiperparametros (Optuna), recogida de feedback y de datos nuevos.
- Avanzado: Docker, base de datos, despliegue, tests unitarios.
- Experto: MLOps (A/B testing, data drift, auto-reemplazo de modelos).

## Tecnologias
Jupyter Notebook, Numpy, Pandas, scikit-learn, Optuna, XGBoost, Matplotlib, Seaborn, Streamlit.

## Dataset
- Fichero: `data/UCI_Credit_Card.csv` (Default of Credit Card Clients, UCI). Clientes de tarjeta de un banco de Taiwan, abril a septiembre de 2005, importes en dolares taiwaneses.
- 30.000 filas, 25 columnas, sin nulos ni duplicados.
- Columnas:
  - `ID`: identificador, se elimina.
  - `LIMIT_BAL`: limite de credito (10.000 a 1.000.000, 81 valores distintos).
  - `SEX`, `EDUCATION`, `MARRIAGE`: codigos categoricos. `AGE`: edad.
  - `PAY_0`, `PAY_2` a `PAY_6`: estado de pago por mes (negativo o 0 al dia, 1 a 8 meses de retraso). `PAY_0` es septiembre; no existe `PAY_1`.
  - `BILL_AMT1` a `BILL_AMT6`: factura mensual (1 es septiembre, 6 es abril).
  - `PAY_AMT1` a `PAY_AMT6`: pago mensual.
  - `default.payment.next.month`: impago al mes siguiente (0/1, 22% de positivos).
- Problemas conocidos:
  - `EDUCATION` con codigos no documentados 0, 5, 6 (345 filas); `MARRIAGE` con 0 (54 filas).
  - Facturas negativas en `BILL_AMT*` (saldo a favor, no es error).
  - Fuerte asimetria en `PAY_AMT*` y `BILL_AMT*`.
  - `BILL_AMT1..6` muy correlacionadas entre si (0,80 a 0,95).

## Variable objetivo y caso de uso
Recomendacion pendiente de confirmar entre Franco y Olena:
- Target: `LIMIT_BAL`.
- Caso de uso: "revision de limite de cliente existente" (perfil mas historial de 6 meses). Medido: R2 de test 0,49 con boosting, frente a 0,18 en el caso "cliente nuevo" (solo perfil).
- No transformar el target con logaritmo (medido: empeora el R2).
- Excluir `default.payment.next.month` (dato futuro; aporta 0,002 de R2).
- Prohibido crear variables que usen `LIMIT_BAL` (por ejemplo factura / limite): es leakage.
- Techo realista: R2 cerca de 0,50, RMSE cerca de 93.000. Un R2 mayor de 0,80 indica leakage.
- Descartado: `BILL_AMT1` como target (R2 alto pero trivial, copia el mes anterior).

Detalle y tabla de cifras en `docs/PLAN.md`.

## Mapa de documentos
- `docs/PLAN.md`: fases, decisiones tecnicas, cifras de referencia, criterio de "hecho".
- `docs/GUIA_PROFESOR.md`: como ensenar cada concepto.
- `docs/TAREAS.md`: reparto, ramas, dependencias y estado.
- `OBSERVACIONES.md`: mensajes entre Franco y Olena (y sus asistentes).
