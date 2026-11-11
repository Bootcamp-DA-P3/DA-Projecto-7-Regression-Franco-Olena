"""Funciones de preprocesamiento compartidas por el notebook y la app.

Se usan dentro del pipeline con FunctionTransformer. Son funciones con nombre
(no lambdas) para que joblib pueda guardar el pipeline entrenado.
"""

import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

# Columnas por grupo (nombres tras renombrar PAY_0 a PAY_1)
COLS_PAY = [f"PAY_{i}" for i in range(1, 7)]
COLS_BILL = [f"BILL_AMT{i}" for i in range(1, 7)]
COLS_PAY_AMT = [f"PAY_AMT{i}" for i in range(1, 7)]
COLS_CATEGORICAS = ["EDUCATION", "MARRIAGE"]
COLS_NUMERICAS = ["AGE"] + COLS_PAY

# Códigos no documentados y la categoría "otros" a la que los pasamos
CODIGOS_OTROS = {
    "EDUCATION": ([0, 5, 6], 4),
    "MARRIAGE": ([0], 3),
}


def agrupar_codigos(X):
    """Pasa los códigos no documentados de EDUCATION y MARRIAGE a "otros"."""
    X = X.copy()
    for col, (codigos, otros) in CODIGOS_OTROS.items():
        if col in X.columns:
            X.loc[X[col].isin(codigos), col] = otros
    return X


def log_con_signo(X):
    """sign(x) * log1p(|x|): reduce la asimetría y conserva el signo de las facturas negativas."""
    return np.sign(X) * np.log1p(np.abs(X))


def crear_preprocesador(incluir_sex=False, usar_log=False):
    """ColumnTransformer con el tratamiento de cada grupo de columnas.

    Las columnas que no están en ningún grupo se descartan (remainder="drop").
    SEX solo entra si incluir_sex=True, para medir cuánto aporta.
    Los logaritmos de los importes solo se aplican si usar_log=True: en la
    sección 8 del notebook empeoran el modelo lineal.
    """
    categoricas = COLS_CATEGORICAS + (["SEX"] if incluir_sex else [])

    tratamiento_categoricas = Pipeline([
        ("agrupar", FunctionTransformer(agrupar_codigos, feature_names_out="one-to-one")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    if usar_log:
        tratamiento_facturas = Pipeline([
            ("log", FunctionTransformer(log_con_signo, feature_names_out="one-to-one")),
            ("escalar", StandardScaler()),
        ])
        tratamiento_pagos = Pipeline([
            ("log", FunctionTransformer(np.log1p, feature_names_out="one-to-one")),
            ("escalar", StandardScaler()),
        ])
    else:
        tratamiento_facturas = StandardScaler()
        tratamiento_pagos = StandardScaler()

    return ColumnTransformer(
        [
            ("categoricas", tratamiento_categoricas, categoricas),
            ("facturas", tratamiento_facturas, COLS_BILL),
            ("pagos", tratamiento_pagos, COLS_PAY_AMT),
            ("numericas", StandardScaler(), COLS_NUMERICAS),
        ],
        remainder="drop",
    )
