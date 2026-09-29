import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from optbinning import OptimalBinning
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform
from scipy.stats import spearmanr

def calcular_estadisticas_categoricas(df, columnas):
    """
    Calcula estadísticas descriptivas para las variables categóricas del DataFrame:
    Variable, Missing, Niveles, Moda, Frec_Moda, Largo.
    """
    filas = []
    for col in columnas:
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

def calcular_estadisticas_numericas(df, columnas):
    """
    Calcula estadísticas descriptivas para las variables numéricas del DataFrame:
    N, valores faltantes, ceros, positivos, negativos, min, max, media,
    percentiles (1%, 5%, 25%, 50%, 75%, 95%, 99%), desvío estándar y
    coeficiente de variación.
    """
    estadisticas = pd.DataFrame({
        'N': df[columnas].count(),
        'N Miss': df[columnas].isnull().sum(),
        'Missing': df[columnas].isnull().mean() * 100,
        'Zeros': (df[columnas] == 0).sum(),
        'Positivos': (df[columnas] > 0).sum(),
        'Negativos': (df[columnas] < 0).sum(),
        'min': df[columnas].min(),
        'max': df[columnas].max(),
        'mean': df[columnas].mean(),
        'p_0.01': df[columnas].quantile(0.01),
        'p_0.05': df[columnas].quantile(0.05),
        'p_0.25': df[columnas].quantile(0.25),
        'p_0.5': df[columnas].quantile(0.5),
        'p_0.75': df[columnas].quantile(0.75),
        'p_0.95': df[columnas].quantile(0.95),
        'p_0.99': df[columnas].quantile(0.99),
        'std': df[columnas].std(),
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

def graficar_clustering_correlacion(df, variables):
    datos = df.loc[:, variables]

    if datos.shape[1] < 2:
        raise ValueError("Se necesitan al menos dos variables.")

    if not all(np.issubdtype(dtype, np.number) for dtype in datos.dtypes):
        raise TypeError("Todas las variables deben ser numéricas.")

    corr = datos.corr(method="spearman").to_numpy()
    corr = np.nan_to_num(corr, nan=0.0)
    corr = (corr + corr.T) / 2
    np.fill_diagonal(corr, 1)

    distance_matrix = 1 - np.abs(corr)
    dist_linkage = hierarchy.ward(squareform(distance_matrix))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))

    dendro = hierarchy.dendrogram(
        dist_linkage,
        labels=variables,
        ax=ax1,
        leaf_rotation=90,
    )

    dendro_idx = np.arange(len(dendro["ivl"]))
    hojas = dendro["leaves"]
    corr_ordenada = corr[hojas, :][:, hojas]

    imagen = ax2.imshow(
        corr_ordenada,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
    )

    ax2.set_xticks(dendro_idx)
    ax2.set_yticks(dendro_idx)
    ax2.set_xticklabels(dendro["ivl"], rotation=90)
    ax2.set_yticklabels(dendro["ivl"])

    # Agregar los valores de correlación con un decimal
    for i in range(corr_ordenada.shape[0]):
        for j in range(corr_ordenada.shape[1]):
            valor = corr_ordenada[i, j]
            color = "white" if abs(valor) >= 0.5 else "black"

            ax2.text(
                j,
                i,
                f"{valor:.1f}",
                ha="center",
                va="center",
                color=color,
                fontsize=8,
            )

    ax2.set_title("Matriz de correlación de Spearman")
    fig.colorbar(imagen, ax=ax2, fraction=0.046, pad=0.04)

    fig.tight_layout()
    return fig, (ax1, ax2)


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

def graficar_boxplot(df: pd.DataFrame, variable_categorica: str, variable_numerica, figsize=None, n_cols=3):
    """
    Genera boxplots de una o varias variables numéricas agrupadas por una variable categórica,
    organizados en una grilla de subplots, usando seaborn.

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame que contiene los datos.
    variable_categorica : str
        Nombre de la columna categórica para el eje x.
    variable_numerica : str o list
        Nombre (o lista de nombres) de la(s) columna(s) numérica(s) para el eje y.
    figsize : tuple, opcional
        Tamaño de la figura completa. Si es None, se calcula automáticamente.
    n_cols : int
        Número de columnas en la grilla de subplots.
    """
    if isinstance(variable_numerica, str):
        variables_numericas = [variable_numerica]
    else:
        variables_numericas = variable_numerica

    n_vars = len(variables_numericas)
    n_cols = min(n_cols, n_vars)
    n_rows = int(np.ceil(n_vars / n_cols))

    if figsize is None:
        figsize = (n_cols * 4, n_rows * 3.5)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    if n_vars == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    for i, var_num in enumerate(variables_numericas):
        ax = axes[i]
        sns.boxplot(data=df, x=variable_categorica, y=var_num, order=["Desertor", "En Curso", "Graduado"], ax=ax)
        ax.set_title(f"{var_num}", fontsize=10)
        ax.set_xlabel(variable_categorica, fontsize=9)
        ax.set_ylabel(var_num, fontsize=9)
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)

    # Ocultar ejes sobrantes
    for j in range(n_vars, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()    

def graficar_barras_apiladas(df: pd.DataFrame, variable_categorica_x: str, variables_categoricas_y, figsize=None, n_cols=3):
    """
    Genera gráficos de barras apiladas al 100% para una o varias variables categóricas
    en función de una variable categórica en el eje x, organizados en una grilla de subplots.

    Parámetros:
    -----------
    df : pd.DataFrame
        DataFrame que contiene los datos.
    variable_categorica_x : str
        Nombre de la columna categórica para el eje x.
    variables_categoricas_y : str o list
        Nombre (o lista de nombres) de la(s) columna(s) categórica(s) a apilar en el eje y.
    figsize : tuple, opcional
        Tamaño de la figura completa. Si es None, se calcula automáticamente.
    n_cols : int
        Número de columnas en la grilla de subplots.
    """
    if isinstance(variables_categoricas_y, str):
        variables_y = [variables_categoricas_y]
    else:
        variables_y = variables_categoricas_y

    n_vars = len(variables_y)
    n_cols = min(n_cols, n_vars)
    n_rows = int(np.ceil(n_vars / n_cols))

    if figsize is None:
        figsize = (n_cols * 12, n_rows * 5)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    if n_vars == 1:
        axes = np.array([axes])
    axes = axes.flatten()

    for i, var_y in enumerate(variables_y):
        ax = axes[i]
        tabla = pd.crosstab(df[variable_categorica_x], df[var_y], normalize='index') * 100
        tabla.plot(kind='bar', stacked=True, ax=ax, colormap='tab20', legend=False)
        ax.set_title(f"{var_y} por {variable_categorica_x}", fontsize=10)
        ax.set_xlabel(variable_categorica_x, fontsize=9)
        ax.set_ylabel("Porcentaje (%)", fontsize=9)
        ax.tick_params(axis='x', rotation=45, labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.legend(title=var_y, bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7)

    # Ocultar ejes sobrantes
    for j in range(n_vars, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()    

def calcular_frecuencias(df, variable):
    """Devuelve la frecuencia y la frecuencia relativa (%) de una variable."""
    if variable not in df.columns:
        raise ValueError(f"La variable '{variable}' no existe en el DataFrame.")

    frecuencias = df[variable].value_counts(dropna=False)
    resultado = pd.DataFrame({
        "Frecuencia": frecuencias,
        "Frecuencia relativa (%)": frecuencias / len(df) * 100,
    })
    resultado.index.name = variable
    return resultado

