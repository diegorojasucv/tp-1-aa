# Predicción y análisis de la deserción universitaria

Trabajo práctico de Aprendizaje Automático sobre la deserción universitaria al finalizar el primer año. El repositorio incluye los datos y su diccionario, notebooks de análisis y modelado, funciones reutilizables, resultados y el informe final. La notebook unificada permite ejecutar el análisis completo desde el CSV original.

## Objetivos

- **Clasificación multiclase:** distinguir entre estudiantes graduados, desertores y en curso.
- **Predicción binaria:** distinguir graduados de desertores con información académica y personal disponible durante el primer año, como paso hacia la estimación del riesgo de abandono en cohortes futuras.
- **Análisis explicativo:** estudiar asociaciones entre predictores y deserción mediante regresión logística e importancia por permutación.

## Contenido del repositorio

```text
.
├── dataset/
│   ├── dataset_TP1_2026.csv              # Datos de entrada
│   └── diccionario_datos_TP1_2026.xlsx   # Diccionario de variables
├── docs/
│   ├── diego_rojas_version/              # Informe individual y guía de formato
│   └── informe_latex/
│       ├── TP1_informe_final.tex          # Fuente LaTeX del informe final
│       ├── TP1_informe_final.pdf          # Informe final compilado
│       └── figuras/                       # Figuras usadas por LaTeX
├── functions/                             # Funciones auxiliares de EDA, entrenamiento y utilidades
├── images/
│   └── informe/                            # Figuras generadas por la notebook unificada
├── notebooks/
│   ├── TP1_desercion_final.ipynb           # Análisis final, de punta a punta
│   ├── resultados.json                     # Resultados numéricos de la ejecución
│   ├── data_cleaning.ipynb                 # Flujo por etapas
│   ├── eda.ipynb
│   ├── training_binario.ipynb
│   └── training_multiclase.ipynb
└── outputs/
    ├── dataset_cleaned.pkl, dataset_binario.pkl, dataset_multiclase.pkl  # artefactos locales, ignorados por Git
    └── modelos/                            # Modelos serializados por tarea
```

## Flujo de trabajo

El punto de entrada recomendado para reproducir los resultados finales es la notebook unificada:

- [Notebook final](notebooks/TP1_desercion_final.ipynb): parte del CSV original, limpia los datos, realiza el análisis exploratorio, entrena y evalúa los modelos binarios y multiclase, y exporta resultados y figuras.

Las notebooks [de limpieza](notebooks/data_cleaning.ipynb), [EDA](notebooks/eda.ipynb), [entrenamiento binario](notebooks/training_binario.ipynb) y [entrenamiento multiclase](notebooks/training_multiclase.ipynb) se conservan como flujos por etapas y materiales de trabajo. Para reproducir el informe vigente, ejecuta la notebook final; conserva la estructura de carpetas para que se resuelvan las rutas relativas. Los archivos `.pkl` procesados y los modelos serializados se encuentran bajo `outputs/`.

## Métodos y evaluación

Se realizan particiones estratificadas de entrenamiento y prueba (80/20) y se seleccionan hiperparámetros mediante validación cruzada estratificada de cinco pliegues. La tarea binaria compara regresión logística, SVM, árbol de decisión y ensambles *Voting*, e incluye Gradient Boosting como referencia. La multiclase compara K-NN, árbol, regresión logística, Random Forest, AdaBoost y XGBoost. La métrica principal es F1-macro.

El análisis exploratorio incluye estadísticas descriptivas, visualizaciones de distribuciones, correlaciones y Valor de Información. Para el modelo explicativo se utiliza regresión logística L1 con un conjunto reducido de predictores e importancia por permutación; también se analizan grupos de variables correlacionadas mediante correlación de Spearman.

## Resultados destacados

- **Multiclase:** XGBoost obtuvo un F1-macro de aproximadamente **0,791** en el conjunto de prueba de la ejecución archivada en `notebooks/resultados.json`. La clase «En curso» fue la más difícil de reconocer.
- **Binario:** el *Voting soft* y Gradient Boosting de referencia obtuvieron un F1-macro de aproximadamente **0,939**, con resultados muy próximos a los modelos base.
- **Modelo explicativo:** la regresión logística reducida destaca el índice de rendimiento académico y la morosidad entre los predictores asociados con la deserción.

Los resultados corresponden a las particiones de prueba de este trabajo y no garantizan el mismo desempeño en otras cohortes. La aplicación futura del modelo binario a estudiantes «En curso» requiere validación con datos prospectivos. Las asociaciones del modelo explicativo no deben interpretarse como relaciones causales, y las predicciones no deben utilizarse como decisiones automáticas sobre trayectorias individuales.

## Requisitos y ejecución

Se necesita **Python 3.11 o posterior** y Jupyter, por ejemplo, mediante VS Code con soporte para notebooks. Instala las dependencias de la notebook final desde [requirements.txt](requirements.txt). Las notebooks por etapas pueden requerir paquetes adicionales —por ejemplo, OptBinning o seaborn— que no forman parte de los requisitos mínimos de la notebook unificada.

## Notebook unificada de la entrega

La notebook de entrega ejecuta el análisis de punta a punta a partir del CSV original:

- [`notebooks/TP1_desercion_final.ipynb`](notebooks/TP1_desercion_final.ipynb): limpieza (incluye eliminación de 313 filas duplicadas), EDA, Valor de Información, **tarea binaria Graduado vs. Desertor** (sin "En curso"; regresión logística, SVM, árbol, *Voting* hard/soft y Gradient Boosting de referencia, con curvas de complejidad por validación cruzada), **aplicación del modelo a los estudiantes "En curso"**, **modelo logístico explicativo** (índice de rendimiento académico, Lasso con regla de 1 error estándar, reajuste con IC 95 %, VIF, importancia por permutación y dependencia parcial por grupos), **tarea multiclase** (K-NN, árbol, Random Forest, AdaBoost, XGBoost) e importancia por permutación por grupos de variables correlacionadas.
- Figuras: `images/informe/`. Resultados numéricos: `notebooks/resultados.json`.
- Informe: [PDF final](docs/informe_latex/TP1_informe_final.pdf) y [fuente LaTeX](docs/informe_latex/TP1_informe_final.tex). Para compilarlo en Overleaf, sube la carpeta `docs/informe_latex/` completa, incluidas sus figuras.

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

   En macOS, instala además la biblioteca OpenMP que necesita XGBoost: `brew install libomp`. Reinicia el kernel si la notebook ya estaba abierta.

2. Abre [`notebooks/TP1_desercion_final.ipynb`](notebooks/TP1_desercion_final.ipynb). En la esquina superior derecha, selecciona como kernel el entorno `.venv` recién creado. Si no aparece, recarga la ventana de VS Code y vuelve a seleccionarlo.
3. Ejecuta las celdas **en orden, desde el principio hasta el final** (en VS Code: **Run All**). La notebook lee el CSV de `dataset/`, crea las figuras en `images/informe/` y guarda `resultados.json` en el directorio de trabajo. Para que quede en `notebooks/`, establece `jupyter.notebookFileRoot` en `${workspaceFolder}/notebooks` en la configuración de VS Code.
4. Espera a que termine la ejecución completa: el entrenamiento y la validación cruzada pueden tardar alrededor de una hora en una máquina de 2 núcleos. No cierres el kernel mientras esté trabajando.

Si aparece `ModuleNotFoundError` (por ejemplo, para `xgboost`), comprueba que el kernel seleccionado sea `.venv` y que instalaste allí las dependencias desde `requirements.txt`; luego reinicia el kernel y vuelve a ejecutar todas las celdas. En macOS, si XGBoost informa que no puede cargar `libxgboost.dylib` por falta de OpenMP, instala `libomp` como se indica arriba.
