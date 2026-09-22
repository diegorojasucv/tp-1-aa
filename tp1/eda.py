import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def calcular_estadisticas_categoricas(df):
    """
    Calcula estadísticas descriptivas para las variables categóricas del DataFrame:
    Variable, Missing, Niveles, Moda, Frec_Moda, Largo.
    """
    columnas_categoricas = df.select_dtypes(include=['object', 'category']).columns

    filas = []
    for col in columnas_categoricas:
        serie = df[col]
        n_missing = serie.isnull().sum()
        niveles = serie.nunique(dropna=True)
        moda_counts = serie.value_counts(dropna=True)
        moda = moda_counts.index[0] if not moda_counts.empty else np.nan
        frec_moda = moda_counts.iloc[0] if not moda_counts.empty else 0
        largo = serie.count()

        filas.append({
            'Variable': col,
            'Missing': n_missing,
            'Niveles': niveles,
            'Moda': moda,
            'Frec_Moda': frec_moda,
            'Largo': largo
        })

    estadisticas = pd.DataFrame(filas).set_index('Variable')

    return estadisticas

def calcular_estadisticas_numericas(df):
    """
    Calcula estadísticas descriptivas para las variables numéricas del DataFrame:
    N, valores faltantes, ceros, positivos, negativos, min, max, media,
    percentiles (1%, 5%, 25%, 50%, 75%, 95%, 99%), desvío estándar y
    coeficiente de variación.
    """
    columnas_numericas = df.select_dtypes(include=[np.number]).columns

    estadisticas = pd.DataFrame({
        'N': df[columnas_numericas].count(),
        'N Miss': df[columnas_numericas].isnull().sum(),
        'Missing': df[columnas_numericas].isnull().mean() * 100,
        'Zeros': (df[columnas_numericas] == 0).sum(),
        'Positivos': (df[columnas_numericas] > 0).sum(),
        'Negativos': (df[columnas_numericas] < 0).sum(),
        'min': df[columnas_numericas].min(),
        'max': df[columnas_numericas].max(),
        'mean': df[columnas_numericas].mean(),
        'p_0.01': df[columnas_numericas].quantile(0.01),
        'p_0.05': df[columnas_numericas].quantile(0.05),
        'p_0.25': df[columnas_numericas].quantile(0.25),
        'p_0.5': df[columnas_numericas].quantile(0.5),
        'p_0.75': df[columnas_numericas].quantile(0.75),
        'p_0.95': df[columnas_numericas].quantile(0.95),
        'p_0.99': df[columnas_numericas].quantile(0.99),
        'std': df[columnas_numericas].std(),
    })

    estadisticas['Coeff of Variation'] = estadisticas['std'] / estadisticas['mean']

    # Reordenar columnas según el orden solicitado
    columnas_orden = [
        'N', 'N Miss', 'Missing', 'Zeros', 'Positivos', 'Negativos',
        'min', 'max', 'mean', 'p_0.01', 'p_0.05', 'p_0.25', 'p_0.5',
        'p_0.75', 'p_0.95', 'p_0.99', 'std', 'Coeff of Variation'
    ]
    estadisticas = estadisticas[columnas_orden]

    return estadisticas


def calcular_correlacion(df, variables=None, metodo="pearson", plot=True, figsize=(12, 8)):
    """Calcula y opcionalmente grafica la matriz de correlación."""
    metodos_validos = {"pearson", "spearman", "kendall"}
    if metodo not in metodos_validos:
        raise ValueError(f"El método debe ser uno de: {sorted(metodos_validos)}")

    if variables is None:
        columnas = df.select_dtypes(include="number").columns.tolist()
    else:
        columnas_faltantes = [columna for columna in variables if columna not in df.columns]
        if columnas_faltantes:
            raise KeyError(f"No existen estas columnas: {columnas_faltantes}")
        columnas = list(variables)

    if len(columnas) < 2:
        raise ValueError("Se necesitan al menos dos variables para calcular correlaciones.")

    columnas_no_numericas = [
        columna for columna in columnas
        if not pd.api.types.is_numeric_dtype(df[columna])
    ]
    if columnas_no_numericas:
        raise TypeError(f"Estas columnas no son numéricas: {columnas_no_numericas}")

    matriz_correlacion = df[columnas].corr(method=metodo)

    if plot:
        fig, ax = plt.subplots(figsize=figsize)
        sns.heatmap(
            matriz_correlacion,
            ax=ax,
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            annot=True,
            fmt=".2f",
            square=True,
            cbar_kws={"label": "Correlación"},
        )
        ax.set_title(f"Matriz de correlación ({metodo})")
        ax.tick_params(axis="x", rotation=90)
        ax.tick_params(axis="y", rotation=0)
        fig.tight_layout()
        plt.show()

    return matriz_correlacion

def calcular_bivariado_iv(df, target_col, variables=None, plot=True):
    """
    Calcula el Information Value (IV) de variables numéricas y categóricas
    usando OptimalBinning.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame con el target y las variables a evaluar.
    target_col : str
        Nombre de la columna target binaria, codificada como 0 y 1.
    variables : list, opcional
        Columnas a evaluar. Si es None, se evalúan todas excepto el target.
    plot : bool
        Si es True, grafica el event rate por bin para cada variable.

    Returns
    -------
    pandas.DataFrame
        Tabla con variable, tipo e IV, ordenada de mayor a menor IV.
    """
    if target_col not in df.columns:
        raise KeyError(f"No existe la columna target: {target_col}")

    target = df[target_col]
    valores_target = set(target.dropna().unique())
    if not valores_target.issubset({0, 1}):
        raise ValueError("El target debe ser binario y estar codificado como 0 y 1.")

    if variables is None:
        variables = [col for col in df.columns if col != target_col]

    variables_faltantes = [col for col in variables if col not in df.columns]
    if variables_faltantes:
        raise KeyError(f"No existen estas columnas: {variables_faltantes}")

    resultados = []

    for var in variables:
        variable = df[var]
        dtype = "numerical" if pd.api.types.is_numeric_dtype(variable) else "categorical"

        try:
            optb_var = OptimalBinning(name=var, dtype=dtype, solver="cp")
            optb_var.fit(variable, target)

            binning_table = optb_var.binning_table
            binning_table.build()
            iv = float(binning_table.iv)
            resultados.append({"variable": var, "tipo": dtype, "iv": iv})

            if plot:
                binning_table.plot(
                    metric="event_rate",
                    add_special=False,
                    add_missing=False,
                    show_bin_labels=True,
                )
                plt.show()

        except Exception as error:
            print(f"Error procesando la variable '{var}': {error}")

    resultado_df = pd.DataFrame(resultados, columns=["variable", "tipo", "iv"])
    return resultado_df.sort_values("iv", ascending=False).reset_index(drop=True)