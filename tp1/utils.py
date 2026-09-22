from pathlib import Path
from typing import Union

import pandas as pd


def guardar_dataframe_pickle(df, nombre_archivo, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    ruta = output_dir / f"{nombre_archivo}.pkl"
    df.to_pickle(ruta)
    print(f"DataFrame guardado en: {ruta.resolve()}")
    return ruta


def cargar_pickle(ruta_archivo: Union[str, Path]):
    """Carga y devuelve el objeto almacenado en un archivo pickle."""
    ruta = Path(ruta_archivo)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    objeto = pd.read_pickle(ruta)
    print(f"Archivo pickle cargado desde: {ruta.resolve()}")
    return objeto

