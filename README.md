# Predicción y análisis de la deserción universitaria

Trabajo práctico de Aprendizaje Automático que analiza datos de estudiantes universitarios para estudiar la deserción al finalizar el primer año. El repositorio contiene el flujo de limpieza y análisis exploratorio, notebooks de entrenamiento y evaluación de modelos, funciones reutilizables, resultados gráficos y modelos serializados.

## Objetivos

- **Clasificación multiclase:** distinguir entre estudiantes graduados, desertores y en curso.
- **Predicción binaria:** distinguir graduados de desertores con información académica y personal disponible durante el primer año, como paso hacia la estimación del riesgo de abandono en cohortes futuras.
- **Análisis explicativo:** estudiar asociaciones entre predictores y deserción mediante regresión logística e importancia por permutación.

## Contenido del repositorio

```text
.
├── dataset/
│   ├── dataset_TP1_2026.csv        # Datos de entrada
│   └── diccionario_datos_TP1_2026.xlsx
├── docs/
│   ├── formato_informe.md          # Guía de formato del trabajo
│   ├── informe_documento_final.md  # Informe final
│   └── informe_documento_final.pdf
├── functions/
│   ├── eda.py                      # Funciones de análisis exploratorio
│   ├── training.py                 # Funciones auxiliares para modelos
│   └── utils.py                    # Utilidades de carga y guardado
├── images/                         # Figuras generadas para el análisis y el informe
├── notebooks/
│   ├── data_cleaning.ipynb
│   ├── eda.ipynb
│   ├── training_binario.ipynb
│   └── training_multiclase.ipynb
└── outputs/
    ├── datasets procesados (.pkl)
    └── modelos entrenados (.pkl)
```

## Flujo de trabajo

Las notebooks principales están pensadas para seguir este orden:

1. [Limpieza de datos](notebooks/data_cleaning.ipynb): lee el archivo CSV, normaliza y transforma variables, y guarda el conjunto limpio.
2. [Análisis exploratorio](notebooks/eda.ipynb): genera estadísticas y visualizaciones, calcula asociaciones e importancia de información, y prepara los conjuntos para las tareas multiclase y binaria.
3. [Entrenamiento binario](notebooks/training_binario.ipynb): compara clasificadores, evalúa el modelo explicativo de regresión logística y guarda los modelos entrenados.
4. [Entrenamiento multiclase](notebooks/training_multiclase.ipynb): compara clasificadores para las tres categorías académicas y guarda los modelos entrenados.

Las notebooks utilizan rutas relativas a `dataset/` y `outputs/`. Ejecútalas con un kernel de Python y conserva la estructura de carpetas del repositorio para que esas rutas se resuelvan correctamente. Los resultados intermedios y los modelos serializados se guardan bajo `outputs/`.

## Métodos y evaluación

Se realizan particiones estratificadas de entrenamiento y prueba (80/20) y se seleccionan hiperparámetros mediante validación cruzada estratificada de cinco pliegues. Se comparan regresión logística, SVM, K-NN, árboles de decisión, Random Forest, Gradient Boosting y un ensamble *Voting (soft)*. La métrica principal de comparación es F1-macro.

El análisis exploratorio incluye estadísticas descriptivas, correlaciones de Spearman, diagramas de caja y Valor de Información. Para el modelo explicativo se utiliza regresión logística L1 con un conjunto reducido de predictores e importancia por permutación.

## Resultados destacados

- **Multiclase:** Gradient Boosting obtuvo un F1-macro de **0,7828** en el conjunto de prueba. La clase «En curso» fue la más difícil de reconocer.
- **Binario:** Gradient Boosting obtuvo un F1-macro de **0,9404** en el conjunto de prueba, con resultados muy próximos a SVM.
- **Modelo explicativo:** la regresión logística reducida destaca el índice de rendimiento académico y la morosidad entre los predictores asociados con la deserción.

Los resultados corresponden a las particiones de prueba de este trabajo y no garantizan el mismo desempeño en otras cohortes. La aplicación futura del modelo binario a estudiantes «En curso» requiere validación con datos prospectivos. Las asociaciones del modelo explicativo no deben interpretarse como relaciones causales, y las predicciones no deben utilizarse como decisiones automáticas sobre trayectorias individuales.

## Requisitos y ejecución

Se necesita **Python 3.10 o posterior** (se recomienda Python 3.11) y un entorno que permita ejecutar notebooks Jupyter (por ejemplo, JupyterLab, Google Colab o VS Code con soporte para notebooks). Las dependencias principales utilizadas incluyen pandas, NumPy, scikit-learn, Matplotlib, seaborn, SciPy, OptBinning, Plotly y statsmodels. Algunas notebooks incluyen celdas para instalar paquetes; el entorno puede requerir dependencias adicionales según las celdas que se ejecuten.

## Versión unificada para la entrega (Martín López y Diego Rojas)

La entrega final combina los dos trabajos del grupo en **una sola notebook** que corre de punta a punta a partir del CSV original:

- [`notebooks/TP1_desercion_final.ipynb`](notebooks/TP1_desercion_final.ipynb): limpieza (incluye eliminación de 313 filas duplicadas), EDA, Valor de Información, **tarea binaria Graduado vs. Desertor** (sin "En curso"; regresión logística, SVM, árbol, *Voting* hard/soft y Gradient Boosting de referencia, con curvas de complejidad por validación cruzada), **aplicación del modelo a los estudiantes "En curso"**, **modelo logístico explicativo** (índice de rendimiento académico, Lasso con regla de 1 error estándar, reajuste con IC 95 %, VIF, importancia por permutación y dependencia parcial por grupos), **tarea multiclase** (K-NN, árbol, Random Forest, AdaBoost, XGBoost) e importancia por permutación por grupos de variables correlacionadas.
- Figuras: `images/informe/`. Resultados numéricos: `notebooks/resultados.json`.
- Informe: [`docs/TP1_informe_final.pdf`](docs/TP1_informe_final.pdf) y su fuente LaTeX para Overleaf en `docs/informe_latex/` (subir la carpeta completa).

### Cómo ejecutar la notebook unificada

1. Instala Python 3.11 y crea un entorno virtual. Usa las instrucciones correspondientes a tu sistema operativo:

   **macOS**

   Si no tienes Homebrew, puedes instalar Python 3.11.x usando el instalador de [python.org](https://www.python.org/downloads/macos/). Si tienes Homebrew:

    ```bash
    brew install python@3.11
    ```

   Abre una terminal nueva, ve a la carpeta raíz del repositorio y crea el entorno:

   ```bash
    python3.11 -m venv .venv
    source .venv/bin/activate
    ```

   **Windows**

   Descarga Python 3.11.x desde [python.org](https://www.python.org/downloads/windows/) y, durante la instalación, marca **Add Python to PATH**. Abre PowerShell en la carpeta raíz del repositorio y crea el entorno:

   ```powershell
   py -3.11 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   Si PowerShell bloquea la activación del entorno, ejecuta `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` una vez y vuelve a activar. Si ya existe `.venv` y fue creada con una versión anterior de Python, elimínala antes de crearla nuevamente con Python 3.11.

   **Instalación de dependencias (macOS y Windows)**

   Con el entorno `.venv` activado, en cualquiera de los dos sistemas ejecuta:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   python -m pip install ipykernel
   ```

    En macOS, instala además la biblioteca OpenMP que necesita XGBoost: `brew install libomp`. Si VS Code ya tenía abierta la notebook, reinicia el kernel después de instalarla para que pueda cargar la biblioteca.

2. Abre [`notebooks/TP1_desercion_final.ipynb`](notebooks/TP1_desercion_final.ipynb). En la esquina superior derecha, selecciona como kernel el entorno `.venv` recién creado. Si no aparece, recarga la ventana de VS Code y vuelve a seleccionarlo.
3. Ejecuta las celdas **en orden, desde el principio hasta el final** (en VS Code: **Run All**). La notebook lee el CSV de `dataset/`, crea las figuras en `images/informe/` y guarda `resultados.json` en el directorio de trabajo. Para que quede en `notebooks/`, establece `jupyter.notebookFileRoot` en `${workspaceFolder}/notebooks` en la configuración de VS Code.
4. Espera a que termine la ejecución completa: el entrenamiento y la validación cruzada pueden tardar alrededor de una hora en una máquina de 2 núcleos. No cierres el kernel mientras esté trabajando.

Si aparece `ModuleNotFoundError` (por ejemplo, para `xgboost`), comprueba que el kernel seleccionado sea `.venv` y que hayas instalado allí las dependencias con `pip install -r requirements.txt`; luego reinicia el kernel y vuelve a ejecutar todas las celdas.
