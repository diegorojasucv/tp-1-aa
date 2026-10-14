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

Se necesita Python 3 y un entorno que permita ejecutar notebooks Jupyter (por ejemplo, JupyterLab, Google Colab o VS Code con soporte para notebooks). Las dependencias principales utilizadas incluyen pandas, NumPy, scikit-learn, Matplotlib, seaborn, SciPy, OptBinning, Plotly y statsmodels. Algunas notebooks incluyen celdas para instalar paquetes; el entorno puede requerir dependencias adicionales según las celdas que se ejecuten.

## Versión unificada para la entrega (Martín López y Diego Rojas)

La entrega final combina los dos trabajos del grupo en **una sola notebook** que corre de punta a punta a partir del CSV original:

- [`notebooks/TP1_desercion_final.ipynb`](notebooks/TP1_desercion_final.ipynb): limpieza (incluye eliminación de 313 filas duplicadas), EDA, Valor de Información, **tarea binaria Graduado vs. Desertor** (sin "En curso"; regresión logística, SVM, árbol, *Voting* hard/soft y Gradient Boosting de referencia, con curvas de complejidad por validación cruzada), **aplicación del modelo a los estudiantes "En curso"**, **modelo logístico explicativo** (índice de rendimiento académico, Lasso con regla de 1 error estándar, reajuste con IC 95 %, VIF, importancia por permutación y dependencia parcial por grupos), **tarea multiclase** (K-NN, árbol, Random Forest, AdaBoost, XGBoost) e importancia por permutación por grupos de variables correlacionadas.
- Figuras: `images/informe/`. Resultados numéricos: `notebooks/resultados.json`.
- Informe: [`docs/TP1_informe_final.pdf`](docs/TP1_informe_final.pdf) y su fuente LaTeX para Overleaf en `docs/informe_latex/` (subir la carpeta completa).
- Dependencias: `pip install -r requirements.txt` (scikit-learn ≥ 1.7). La corrida completa tarda alrededor de 1 hora en una máquina de 2 núcleos.

Cambios respecto de las notebooks originales de la parte binaria: se estandarizan las variables numéricas dentro del `Pipeline` (antes solo se aplicaba *one-hot*), la SVM busca también `gamma`, el *Voting* combina los modelos pedidos por la consigna (LR + SVM + árbol), las curvas de complejidad se calculan con validación cruzada (no con el test) y se eliminan los duplicados. Los resultados se mantienen muy cercanos a los originales (F1-macro binario ≈ 0,94).

## Informe

El informe completo se encuentra en [formato Markdown](docs/informe_documento_final.md) y [formato PDF](docs/informe_documento_final.pdf). La guía de presentación del trabajo está en [docs/formato_informe.md](docs/formato_informe.md).
