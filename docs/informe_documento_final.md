**Trabajo Práctico 1 - Aprendizaje Automático**  
**Estudiante:** Diego Rojas  
**Tema:** Determinantes de la deserción universitaria y predicción

## Resumen

Este trabajo analiza variables asociadas con la deserción universitaria y compara modelos para clasificar la situación académica de los estudiantes. Se utilizó un conjunto de datos de 50.000 registros y se abordaron dos tareas: una clasificación multiclase de graduados, desertores y estudiantes en curso, y una clasificación binaria de graduados y desertores. Los datos se dividieron en entrenamiento y prueba en una proporción de 80/20, con estratificación, y los hiperparámetros se seleccionaron mediante validación cruzada estratificada de cinco pliegues. El mejor resultado multiclase fue de Gradient Boosting, con un F1-macro de 0,783; para la tarea binaria, el mayor F1-macro fue 0,940, también con Gradient Boosting. En el modelo logístico explicativo, el índice de rendimiento académico y la morosidad concentraron la mayor capacidad predictiva según la importancia por permutación. Estos resultados muestran que el rendimiento del primer año aporta información relevante para distinguir los estados académicos, aunque la clasificación de estudiantes que continúan en curso es menos precisa. Las asociaciones observadas no deben interpretarse como causales y el modelo requiere validación adicional antes de un uso institucional.

## Introducción

El objetivo de este trabajo es predecir qué estudiantes desertarán al finalizar el primer año universitario, utilizando información académica y personal disponible hasta ese momento. Identificar entonces a estudiantes que podrían necesitar apoyo puede ayudar a áreas como Bienestar Estudiantil o Secretaría Académica a planificar intervenciones oportunas; las predicciones, sin embargo, no deben utilizarse como decisiones automáticas sobre las trayectorias individuales.

La literatura teórica (Tinto, 1975, 1993; Bean, 1980; Bean y Metzner, 1985) y empírica (Yorke y Longden, 2004; OECD, 2019) caracteriza la deserción como un fenómeno multicausal, relacionado con factores individuales, institucionales, socioeconómicos y de integración académica. Como la relevancia de estos factores puede variar según el contexto, este estudio evalúa cuáles resultan más informativos en el conjunto de datos analizado, sin asumir que las asociaciones estimadas sean causales.

La pregunta central es **¿qué variables permiten distinguir y predecir mejor la deserción universitaria a partir de la información del primer año?** Para responderla, se realiza un análisis exploratorio y se comparan dos tareas: una clasificación multiclase (graduado, desertor y en curso), que permite examinar especialmente la identificación de quienes continúan estudiando, y una clasificación binaria (graduado o desertor), que excluye los casos en curso. Se plantea como hipótesis que el desempeño académico, la situación financiera, la edad y algunas características de ingreso aportan información predictiva. El informe presenta los datos y el procedimiento, los resultados de ambas tareas y, finalmente, sus alcances y limitaciones.

## Materiales y métodos

Se utilizó el conjunto de datos universitario provisto para el trabajo práctico, con 50.000 registros y 27 variables originales. Las variables se renombraron con el formato *lower_snake_case*. Algunas variables categóricas se recodificaron como indicadores binarios y se construyeron variables numéricas derivadas mediante promedios y razones entre variables existentes. No se dispone de información adicional sobre el procedimiento de recolección de los datos, por lo que no es posible evaluar su representatividad más allá de la muestra analizada.

### i) Datos y variables explicativas (E)

El conjunto original contiene 50.000 registros y 27 variables. En las variables analizadas no se detectaron valores faltantes; además, las variables numéricas de edad, puntajes y unidades curriculares no presentan valores negativos. La Tabla 1 resume los estadísticos de las principales variables numéricas y la Tabla 2 presenta la cantidad de niveles y la categoría más frecuente de las variables categóricas consideradas. La ausencia de valores faltantes y negativos es consistente con lo esperado, aunque no permite descartar otros posibles problemas de calidad o sesgos en el origen de los datos. En particular, la variable denominada `ratio_aprobadas_inscritas` tiene un máximo de 1,80; si representa estrictamente unidades aprobadas sobre inscritas, conviene revisar cómo se construyó ese valor, ya que supera el límite esperado de 1.

Tabla 1. *Resumen descriptivo de las variables numéricas del conjunto de datos ($N = 50.000$)*

| Variable | $N$ | Faltantes | Faltantes (%) | Ceros | Positivos | Negativos | Mín. | Máx. | Media | $p_{0.01}$ | $p_{0.05}$ | $p_{0.25}$ | $p_{0.50}$ | $p_{0.75}$ | $p_{0.95}$ | $p_{0.99}$ | DE | CV |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **cualificacion_promedio** | 50.000 | 0 | 0,00 % | 0 | 50.000 | 0 | 48,00 | 95,00 | 66,26 | 51,99 | 58,00 | 62,00 | 67,00 | 70,00 | 75,00 | 80,00 | 5,52 | 0,08 |
| **puntaje_ingreso** | 50.000 | 0 | 0,00 % | 0 | 50.000 | 0 | 48,00 | 95,00 | 62,67 | 49,00 | 52,00 | 59,00 | 62,00 | 66,00 | 75,00 | 80,00 | 6,28 | 0,10 |
| **edad_inscripcion** | 50.000 | 0 | 0,00 % | 0 | 50.000 | 0 | 17,00 | 70,00 | 22,28 | 18,00 | 18,00 | 18,00 | 19,00 | 23,00 | 38,00 | 49,00 | 6,90 | 0,31 |
| **es_masculino** | 50.000 | 0 | 0,00 % | 34.240 | 15.760 | 0 | 0,00 | 1,00 | 0,32 | 0,00 | 0,00 | 0,00 | 0,00 | 1,00 | 1,00 | 1,00 | 0,46 | 1,47 |
| **es_desplazado** | 50.000 | 0 | 0,00 % | 21.452 | 28.548 | 0 | 0,00 | 1,00 | 0,57 | 0,00 | 0,00 | 0,00 | 1,00 | 1,00 | 1,00 | 1,00 | 0,49 | 0,87 |
| **es_asistencia_diurna** | 50.000 | 0 | 0,00 % | 4.244 | 45.756 | 0 | 0,00 | 1,00 | 0,92 | 0,00 | 0,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 0,28 | 0,30 |
| **es_deudor** | 50.000 | 0 | 0,00 % | 46.424 | 3.576 | 0 | 0,00 | 1,00 | 0,07 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,00 | 1,00 | 0,26 | 3,60 |
| **es_moroso** | 50.000 | 0 | 0,00 % | 5.361 | 44.639 | 0 | 0,00 | 1,00 | 0,89 | 0,00 | 0,00 | 1,00 | 1,00 | 1,00 | 1,00 | 1,00 | 0,31 | 0,35 |
| **es_becado** | 50.000 | 0 | 0,00 % | 37.622 | 12.378 | 0 | 0,00 | 1,00 | 0,25 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 1,00 | 1,00 | 0,43 | 1,74 |
| **es_estudiante_internacional** | 50.000 | 0 | 0,00 % | 49.671 | 329 | 0 | 0,00 | 1,00 | 0,01 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,08 | 12,29 |
| **tiene_necesidades_educativas_especiales** | 50.000 | 0 | 0,00 % | 49.808 | 192 | 0 | 0,00 | 1,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,06 | 16,11 |
| **promedio_notas_semestres** | 50.000 | 0 | 0,00 % | 10.124 | 39.876 | 0 | 0,00 | 91,00 | 49,12 | 0,00 | 0,00 | 51,00 | 60,50 | 66,00 | 72,50 | 76,00 | 26,22 | 0,53 |
| **promedio_uc_inscritos_semestres** | 50.000 | 0 | 0,00 % | 1.744 | 48.256 | 0 | 0,00 | 21,00 | 5,92 | 0,00 | 5,00 | 5,00 | 6,00 | 6,00 | 8,00 | 11,50 | 1,64 | 0,28 |
| **promedio_uc_aprobadas_semestres** | 50.000 | 0 | 0,00 % | 10.127 | 39.873 | 0 | 0,00 | 20,00 | 4,10 | 0,00 | 0,00 | 1,50 | 5,00 | 6,00 | 7,50 | 10,00 | 2,68 | 0,65 |
| **promedio_cant_evaluaciones_semestres** | 50.000 | 0 | 0,00 % | 5.065 | 44.935 | 0 | 0,00 | 33,00 | 7,32 | 0,00 | 0,00 | 6,00 | 7,50 | 9,00 | 12,50 | 15,50 | 3,32 | 0,45 |
| **ratio_aprobadas_inscritas** | 50.000 | 0 | 0,00 % | 10.131 | 39.869 | 0 | 0,00 | 1,80 | 0,65 | 0,00 | 0,00 | 0,30 | 0,83 | 1,00 | 1,00 | 1,00 | 0,39 | 0,60 |
| **ingresos_familia_nivel** | 50.000 | 0 | 0,00 % | 0 | 50.000 | 0 | 1,00 | 5,00 | 2,24 | 1,00 | 1,00 | 1,00 | 2,00 | 3,00 | 4,50 | 5,00 | 1,12 | 0,50 |
| **demanda_cog_familia_nivel** | 50.000 | 0 | 0,00 % | 0 | 50.000 | 0 | 1,00 | 5,00 | 2,24 | 1,00 | 1,00 | 1,00 | 2,00 | 3,00 | 4,50 | 5,00 | 1,12 | 0,50 |

<small>Estadísticos descriptivos, percentiles y frecuencias de valores faltantes y ceros. $N$ = número de registros; Positivos/Negativos = valores mayores/menores que cero; DE = desviación estándar; CV = coeficiente de variación (DE / media); $p_{0.01}$ a $p_{0.99}$ = percentiles 1, 5, 25, 50, 75, 95 y 99; uc = unidades curriculares. En las variables binarias, los ceros y positivos indican las frecuencias de las categorías 0 y 1, respectivamente.</small>

Tabla 2. *Resumen descriptivo de las variables categóricas del modelo ($N = 50.000$)*

| Variable | Faltantes | Niveles | Moda | Frecuencia de la moda | Registros |
| :--- | :---: | :---: | :--- | :---: | :---: |
| **Estudios_máximos_antes_de_la_inscripción** | 0 | 5 | Educación Secundaria | 43.950 | 50.000 |
| **estado_civil** | 0 | 6 | Soltero | 45.861 | 50.000 |
| **modo_aplicacion** | 0 | 4 | Acceso General | 34.694 | 50.000 |
| **macro_categoria_carrera** | 0 | 6 | Comunicación, marketing y diseño | 12.490 | 50.000 |

<small>Propiedades de las variables categóricas. Niveles = cantidad de categorías distintas; Moda = categoría más frecuente; Frecuencia de la moda = número de registros en esa categoría; Registros = total de observaciones analizadas.</small>


### ii) Variable respuesta y tarea objetivo (T)

La variable respuesta es `target`, con tres estados: **Graduado**, **Desertor** y **En curso**. En la tarea multiclase se conservaron las tres categorías. Para la tarea binaria se excluyeron los casos **En curso** y se clasificaron únicamente los registros con estado **Graduado** o **Desertor**. Por lo tanto, esta tarea estima la probabilidad de pertenecer a uno de esos dos estados dentro de la muestra analizada; no clasifica el estado de quienes siguen en curso.

Para la clasificación multiclase, las etiquetas se codificaron de la siguiente manera:
  - Graduado igual a 0
  - Desertor igual a 1
  - En Curso igual a 2

La Tabla 3 muestra que graduados y desertores representan, respectivamente, el 47,41 % y el 33,06 % de la muestra completa, mientras que el 19,53 % permanece en curso. La distribución no está equilibrada por completo; por ello se estratificaron las particiones y se utilizó F1-macro, que asigna el mismo peso a cada clase, en vez de basar la comparación únicamente en la clase más frecuente.

Tabla 3. *Distribución de frecuencias de la variable objetivo (target) ($N = 50.000$)*

| Variable | Frecuencia | Frecuencia relativa (%) |
| :--- | :---: | :---: |
| **Graduado** | 23.707 | 47,41 % |
| **Desertor** | 16.529 | 33,06 % |
| **En Curso** | 9.764 | 19,53 % |

<small>Distribución de categorías de la variable dependiente u objetivo (target) del estudio. Variable = Estado académico final del estudiante; Frecuencia = Número absoluto de estudiantes en cada categoría; Frecuencia relativa (%) = Porcentaje respecto al total de la muestra analizada ($N = 50.000$).</small>


### iii) Manejo de datos y esquemas de clasificación

#### Análisis exploratorio de los datos

El análisis exploratorio se realizó antes de ajustar los modelos. La Figura 1 presenta el agrupamiento jerárquico y la matriz de correlación de Spearman para las variables numéricas. Se observa una asociación alta entre las unidades curriculares inscritas y aprobadas y las notas de ambos semestres (en varios pares, aproximadamente entre 0,8 y 1,0). También se observa una correlación negativa de alrededor de -0,5 entre los indicadores de deuda y morosidad. Estas relaciones indican que algunas variables contienen información redundante; por eso, para el modelo logístico explicativo se redujo el conjunto de predictores académicos y se construyó un índice compuesto. La correlación, por sí sola, no demuestra que una variable sesgue la importancia de otra ni permite inferir causalidad.

![Matriz de correlación de las variables numéricas](../images/corr_todas_variables.png)
Figura 1. *Agrupamiento jerárquico y matriz de correlación de Spearman de las variables numéricas.* Los valores de la matriz representan correlaciones por rangos; el agrupamiento muestra qué variables presentan patrones de asociación similares.

La Figura 2 compara las distribuciones de seis variables numéricas según el estado académico. El promedio de notas y la razón de unidades aprobadas sobre inscritas muestran diferencias más marcadas entre desertores y graduados. En cambio, algunas distribuciones de graduados y estudiantes en curso se superponen, aunque esto no implica que ambos estados sean equivalentes. Esta superposición ayuda a contextualizar la dificultad del modelo multiclase para identificar correctamente la categoría en curso, como se verá en la Tabla 6.

![Diagramas de caja de las principales variables numéricas por estado académico](../images/boxplot.png)
Figura 2. *Distribución de variables numéricas según la categoría de `target`.* Las líneas centrales representan las medianas, las cajas el rango intercuartílico y los puntos las observaciones atípicas.

La Tabla 4 ordena las variables por su Valor de Información (IV), calculado para distinguir las categorías graduado y desertor en la tarea binaria. El mayor valor corresponde a `ratio_aprobadas_inscritas` (5,38), seguido por `promedio_notas_semestres` (4,33), el promedio de evaluaciones (1,65), la morosidad (1,42) y la condición de becario (0,97). El orden sugiere que el rendimiento académico y ciertas variables financieras aportan información para separar los dos estados. Sin embargo, IV no mide causalidad ni equivale al desempeño de un modelo; los valores particularmente elevados deben leerse como señales de asociación intensa y revisarse teniendo en cuenta la definición y el momento de medición de las variables.

Tabla 4. *Valor de Información (IV) por variable predictora*

| Variable | Tipo | IV |
| :--- | :---: | :---: |
| **ratio_aprobadas_inscritas** | Numérica | 5,38 |
| **promedio_notas_semestres** | Numérica | 4,33 |
| **promedio_cant_evaluaciones_semestres** | Numérica | 1,65 |
| **es_moroso** | Categórica | 1,42 |
| **es_becado** | Categórica | 0,97 |
| **edad_inscripcion** | Numérica | 0,89 |
| **carrera** | Categórica | 0,85 |
| **modo_aplicacion** | Categórica | 0,63 |
| **sexo** | Categórica | 0,57 |
| **tiene_deuda** | Categórica | 0,34 |

<small>Valor de Información (IV) por variable candidata para la tarea binaria graduado/desertor. IV resume la capacidad de separación asociada a cada predictor; sus valores no son porcentajes ni efectos causales y dependen del procedimiento de agrupación utilizado.</small>

#### Partición del conjunto de datos

Para cada tarea se dividieron los datos en conjuntos de entrenamiento y prueba en una proporción de 80/20, con `random_state=42` y estratificación según la variable objetivo. La búsqueda de hiperparámetros se realizó mediante validación cruzada estratificada de cinco pliegues sobre el conjunto de entrenamiento; el preprocesamiento categórico se ajustó dentro de los *pipelines* para evitar fuga de información entre pliegues. Se compararon los modelos con F1-macro, que promedia el F1 de cada clase con igual peso y resulta pertinente ante la distribución desigual de las categorías. Esta métrica no elimina el desbalance ni sustituye el examen de los errores por clase, por lo que también se presenta la matriz de confusión multiclase. Los F1 reportados en las Tablas 5 y 7 corresponden al conjunto de prueba.

El preprocesamiento de los modelos comparativos codificó las variables categóricas mediante *one-hot encoding*. Las variables numéricas se conservaron en sus escalas originales, excepto las usadas en el índice del modelo explicativo. Esta decisión debe tenerse en cuenta al interpretar los resultados de SVM, K-NN y la regresión logística regularizada, que pueden ser sensibles a la escala de los predictores.

## Resultados

### Clasificación multiclase

En la clasificación multiclase se compararon los modelos y las estrategias resumidos en la Tabla 5. En las regresiones logísticas se evaluaron los esquemas *one-vs-rest* (OvR) y *one-vs-one* (OvO); SVM implementó OvO y los demás clasificadores admitieron las tres clases directamente. Gradient Boosting obtuvo el mayor F1-macro (0,783), seguido por Random Forest (0,777) y SVM (0,773). La diferencia entre el mejor modelo y SVM es pequeña, por lo que no debe interpretarse como una ventaja concluyente sin evaluar la variabilidad de las particiones.

Tabla 5. *Resultados del ajuste de hiperparámetros y evaluación de modelos de clasificación*

| Modelo | Estrategia multiclase | Hiperparámetros y rangos evaluados | Valores finales | F1-score |
| :--- | :--- | :--- | :--- | :---: |
| **Regresión Logística (One-vs-Rest)** | One-vs-Rest (OvR) | `penalty`: ["l1", "l2", "elasticnet"]<br>`C`: [0.001, 0.01, 0.1, 1, 10, 100]<br>`l1_ratio`: [0.1, 0.5, 0.9] *(para elasticnet)* | `penalty`: 'elasticnet'<br>`C`: 1<br>`l1_ratio`: 0.9 | 0,7613 |
| **Regresión Logística (One-vs-One)** | One-vs-One (OvO) | `penalty`: ["l1", "l2", "elasticnet"]<br>`C`: [0.001, 0.01, 0.1, 1, 10, 100]<br>`l1_ratio`: [0.1, 0.5, 0.9] *(para elasticnet)* | `penalty`: 'l1'<br>`C`: 10 | 0,7725 |
| **SVM** *(SVC)* | One-vs-One (OvO nativo) | `C`: [0.1, 1, 10, 100] | `C`: 100 | 0,7734 |
| **K-NN** | Directa (Multiclase nativa) | `n_neighbors`: [3, 5, 7, 9, 11, 13, 15] | `n_neighbors`: 15 | 0,7318 |
| **Bagging / Random Forest** | Directa (Multiclase nativa) | `n_estimators`: [100, 200, 400]<br>`max_depth`: [None, 5, 10, 20]<br>`min_samples_split`: [2, 5, 10]<br>`min_samples_leaf`: [1, 2, 4]<br>`max_features`: ["sqrt", "log2"] | `n_estimators`: 200<br>`max_depth`: 20<br>`min_samples_split`: 10<br>`min_samples_leaf`: 1<br>`max_features`: 'sqrt' | 0,7768 |
| **Árbol de decisión** | Directa (Multiclase nativa) | `criterion`: ["gini", "entropy"]<br>`max_depth`: [None, 3, 5, 10, 20]<br>`min_samples_split`: [2, 5, 10]<br>`min_samples_leaf`: [1, 2, 4] | `criterion`: 'gini'<br>`max_depth`: 5<br>`min_samples_leaf`: 4<br>`min_samples_split`: 2 | 0,7690 |
| **Boosting** *(Gradient Boosting)* | Directa (Multiclase nativa) | `n_estimators`: [100, 200]<br>`learning_rate`: [0.01, 0.1, 0.2]<br>`max_depth`: [2, 3, 5]<br>`subsample`: [0.8, 1.0] | `n_estimators`: 100<br>`learning_rate`: 0.1<br>`max_depth`: 5<br>`subsample`: 0.8 | 0,7828 |

<small>Hiperparámetros seleccionados mediante búsqueda en rejilla (GridSearchCV) y validación cruzada estratificada de cinco pliegues; F1-macro calculado en el conjunto de prueba y redondeado a cuatro decimales. SVM = máquina de soporte vectorial; K-NN = vecinos más cercanos; OvR = uno contra el resto; OvO = uno contra uno.</small>

La Tabla 6 detalla los aciertos y errores del mejor modelo multiclase. Las filas son las categorías reales y las columnas las predichas; la codificación es 0 = graduado, 1 = desertor y 2 = en curso. El modelo identifica correctamente el 91,9 % de los graduados (4.356 de 4.741) y el 81,6 % de los desertores (2.698 de 3.306), pero el 59,5 % de los estudiantes en curso (1.163 de 1.953). Entre estos últimos, el 28,8 % se clasifica como graduado. Por tanto, existe una dificultad relativa para reconocer la categoría en curso, pero estos resultados no justifican combinarla con graduados: son estados académicos distintos y la matriz evidencia errores de clasificación, no equivalencia entre las categorías.

Tabla 6. *Matriz de confusión del mejor modelo seleccionado (Gradient Boosting)*

| | Predicho: Clase 0 | Predicho: Clase 1 | Predicho: Clase 2 | Total Real |
| :--- | :---: | :---: | :---: | :---: |
| **Real: Clase 0** | **4.356** | 62 | 323 | 4.741 |
| **Real: Clase 1** | 241 | **2.698** | 367 | 3.306 |
| **Real: Clase 2** | 562 | 228 | **1.163** | 1.953 |
| **Total Predicho** | 5.159 | 2.988 | 1.853 | 10.000 |

<small>Matriz de confusión de Gradient Boosting en el conjunto de prueba ($N = 10.000$). Filas = clase real; columnas = clase predicha; la diagonal contiene los aciertos y las restantes celdas, los errores.</small>

### Clasificación binaria

En la tarea binaria se conservaron 40.236 registros (graduados y desertores) y se compararon los modelos de la Tabla 7. Gradient Boosting alcanzó el F1-macro más alto (0,940), seguido muy de cerca por SVM (0,940) y regresión logística (0,938); el ensamble *Voting (soft)* obtuvo 0,939 y K-NN, 0,914. La diferencia entre Gradient Boosting y SVM es mínima al nivel de redondeo presentado, y el ensamble no superó a los modelos individuales. Como análisis complementario, se utiliza una regresión logística con un conjunto reducido de variables para facilitar la interpretación; esta no es la misma configuración del modelo comparativo de mejor puntuación.

Tabla 7. *Resumen de optimización de hiperparámetros y F1-score por modelo de clasificación*

| Modelo | Hiperparámetros y rangos evaluados | Valores finales | F1-score |
| :--- | :--- | :--- | :---: |
| **Regresión logística** | `penalty`: ["l1", "l2", "elasticnet"]<br>`C`: [0.001, 0.01, 0.1, 1, 10, 100]<br>`l1_ratio`: [0.1, 0.5, 0.9] *(para elasticnet)* | `penalty`: 'l1'<br>`C`: 1 | 0,9383 |
| **SVM** | `C`: [0.1, 1, 10, 100] | `C`: 100 | 0,9403 |
| **K-NN** | `n_neighbors`: [3, 5, 7, 9, 11, 13, 15] | `n_neighbors`: 13 | 0,9142 |
| **Random Forest** | `n_estimators`: [100, 200, 400]<br>`max_depth`: [None, 5, 10, 20]<br>`min_samples_split`: [2, 5, 10]<br>`min_samples_leaf`: [1, 2, 4]<br>`max_features`: ["sqrt", "log2"] | `n_estimators`: 400<br>`max_depth`: 20<br>`min_samples_split`: 5<br>`min_samples_leaf`: 1<br>`max_features`: 'sqrt' | 0,9381 |
| **Árbol de decisión** | `max_depth`: [None, 3, 5, 10, 20]<br>`min_samples_split`: [2, 5, 10]<br>`min_samples_leaf`: [1, 2, 4]<br>`criterion`: ["gini", "entropy"] | `max_depth`: 5<br>`min_samples_leaf`: 2<br>`min_samples_split`: 2<br>`criterion`: 'gini' | 0,9338 |
| **Gradient Boosting** | `n_estimators`: [100, 200]<br>`learning_rate`: [0.01, 0.1, 0.2]<br>`max_depth`: [2, 3, 5]<br>`subsample`: [0.8, 1.0] | `n_estimators`: 200<br>`learning_rate`: 0.1<br>`max_depth`: 3<br>`subsample`: 0.8 | 0,9404 |
| **Voting (soft)** | Combinación de regresión logística, SVM y Random Forest | `voting`: 'soft' | 0,9394 |

<small>Hiperparámetros seleccionados mediante GridSearchCV con validación cruzada estratificada de cinco pliegues; F1-macro calculado en el conjunto de prueba y redondeado a cuatro decimales. Voting (soft) combina las probabilidades de regresión logística, SVM y Random Forest; SVM = máquina de soporte vectorial; K-NN = vecinos más cercanos.</small>

Para el análisis logístico explicativo se seleccionó un conjunto reducido de predictores. El promedio de notas y la razón entre unidades aprobadas e inscritas se estandarizaron usando la media y el desvío calculados solo sobre entrenamiento; luego se promediaron para formar `indice_rendimiento_academico`, y se retiraron del modelo las dos variables originales. La Figura 3 muestra que, en este conjunto final, las correlaciones absolutas entre los predictores son moderadas (la mayor se aproxima a 0,4), en contraste con algunos pares de variables académicas de la Figura 1. Esto reduce la redundancia lineal observada, aunque no demuestra independencia entre las variables.

![Agrupamiento y correlación de las variables del modelo explicativo](../images/corr_variables_seleccionadas.png)
Figura 3. *Agrupamiento jerárquico y matriz de correlación de Spearman de las variables seleccionadas.* El índice de rendimiento combina las variables académicas estandarizadas; no equivale a una medida de efecto causal.

En el conjunto de prueba, la regresión logística explicativa obtiene un F1-macro cercano a 0,94, comparable al de la versión con más variables (Tabla 7). La similitud del resultado sugiere que el conjunto reducido conserva gran parte de la capacidad predictiva medida por F1-macro, aunque la comparación no demuestra que el índice sea la única fuente de información redundante ni que el modelo simplificado sea superior.

### Modelo logístico explicativo

#### Coeficientes del modelo

La Tabla 8 presenta los coeficientes estimados mediante regresión logística sobre el conjunto de entrenamiento de la tarea binaria. El resultado del modelo se codificó como 1 para deserción, de modo que un coeficiente positivo se asocia con mayores log-odds de deserción y uno negativo con menores log-odds, manteniendo constantes los demás predictores. El índice de rendimiento académico tiene un coeficiente negativo grande (-3,330), mientras que la morosidad presenta un coeficiente positivo (3,469); ambos son estadísticamente distintos de cero según sus intervalos de confianza. También aparecen asociaciones positivas con el promedio de evaluaciones, la edad y el indicador masculino, y negativas con la condición de becario, el puntaje de ingreso y los ingresos familiares. Los coeficientes de las categorías se interpretan respecto de sus categorías de referencia, que no se muestran en la tabla. Estas estimaciones describen asociaciones condicionales en la muestra y no efectos causales.

Tabla 8. *Resultados de la regresión logística (Logit)*

| Variable | Coeficiente ($\beta$) | Error estándar | Valor z | p-valor | IC 95% Inferior | IC 95% Superior |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Intercepto** | 0,178 | 0,371 | 0,480 | 0,631 | -0,550 | 0,906 |
| **Estudios máximos: Educación Secundaria** | -0,190 | 0,134 | -1,422 | 0,155 | -0,453 | 0,072 |
| **Estudios máximos: Otro** | 0,556 | 0,671 | 0,828 | 0,408 | -0,759 | 1,871 |
| **Estudios máximos: Superior - Pregrado** | -0,356 | 0,159 | -2,241 | 0,025 | -0,667 | -0,045 |
| **Estado civil: Otro** | 0,353 | 0,212 | 1,668 | 0,095 | -0,062 | 0,768 |
| **Estado civil: Soltero** | 0,417 | 0,122 | 3,420 | 0,001 | 0,178 | 0,656 |
| **Carrera: Ciencias agropecuarias y veterinarias** | -0,242 | 0,082 | -2,937 | 0,003 | -0,403 | -0,080 |
| **Carrera: Ciencias sociales** | -0,343 | 0,072 | -4,767 | <0,001 | -0,485 | -0,202 |
| **Carrera: Comunicación, marketing y diseño** | -0,586 | 0,071 | -8,298 | <0,001 | -0,725 | -0,448 |
| **Carrera: Ingeniería y tecnología** | 1,383 | 0,179 | 7,708 | <0,001 | 1,032 | 1,735 |
| **Carrera: Salud** | -0,892 | 0,081 | -11,033 | <0,001 | -1,051 | -0,734 |
| **Puntaje de ingreso** | -0,037 | 0,004 | -8,993 | <0,001 | -0,045 | -0,029 |
| **Edad de inscripción** | 0,024 | 0,005 | 4,753 | <0,001 | 0,014 | 0,034 |
| **Tiene necesidades educativas especiales** | 0,812 | 0,316 | 2,571 | 0,010 | 0,193 | 1,431 |
| **Es masculino** | 0,513 | 0,054 | 9,449 | <0,001 | 0,406 | 0,619 |
| **Es moroso** | 3,469 | 0,140 | 24,834 | <0,001 | 3,195 | 3,743 |
| **Es becado** | -1,353 | 0,067 | -20,127 | <0,001 | -1,485 | -1,221 |
| **Es estudiante internacional** | -0,815 | 0,297 | -2,745 | 0,006 | -1,396 | -0,233 |
| **Promedio cantidad evaluaciones semestres** | 0,247 | 0,009 | 28,404 | <0,001 | 0,230 | 0,264 |
| **Ingresos familia nivel** | -0,099 | 0,022 | -4,574 | <0,001 | -0,142 | -0,057 |
| **Índice rendimiento académico** | -3,330 | 0,044 | -75,125 | <0,001 | -3,417 | -3,243 |

<small>Modelo Logit estimado por máxima verosimilitud con el conjunto de entrenamiento ($N = 32.188$); grados de libertad = 20; pseudo-$R^2$ = 0,709; log-verosimilitud = -6.351,5; prueba de razón de verosimilitud, $p < 0,001$. $\beta$ = coeficiente en escala log-odds; IC 95 % = intervalo de confianza al 95 %. Para las variables categóricas, los coeficientes se comparan con la categoría de referencia omitida durante la codificación.</small>

#### Curva de complejidad y análisis de importancia

La Figura 4 muestra la curva de complejidad de la regresión logística con regularización L1. El eje horizontal presenta $C$, inverso de la fuerza de regularización: a menor $C$, mayor penalización. El F1-macro de entrenamiento y prueba crece con rapidez en los valores más pequeños de $C$ y se estabiliza alrededor de 0,92–0,93 desde aproximadamente $C=0,01$; las curvas permanecen próximas en el rango mostrado. Esto no presenta una brecha evidente entre entrenamiento y prueba, aunque no basta para descartar sobreajuste: la curva usa el conjunto de prueba para varios valores de $C$ y debe interpretarse como exploratoria, no como una validación independiente.

![Curva de complejidad de la regresión logística con regularización L1](../images/curvas_complejidad_rl_lasso.png)
Figura 4. *F1-macro en entrenamiento y prueba para distintos valores de $C$.* Un valor menor de $C$ implica una regularización más intensa.

La Figura 5 muestra la trayectoria de los coeficientes del modelo Lasso al variar $C$. Al aumentar $C$ y disminuir la regularización, los coeficientes se alejan de cero y luego se estabilizan. Este gráfico muestra cómo cambia el ajuste de los coeficientes, pero no debe confundirse con una medida directa de importancia ni con la curva de desempeño de la Figura 4.

![Evolución de los coeficientes de la regresión logística con regularización L1](../images/coeficientes_por_regularizacion.png)
Figura 5. *Trayectoria de los coeficientes para distintos valores de $C$.* La línea horizontal discontinua marca el valor cero.

La importancia por permutación de la Figura 6 se calculó midiendo la disminución del F1-macro al permutar cada variable. En el conjunto de prueba, el índice de rendimiento académico presenta la mayor disminución (aproximadamente 0,31), seguido por la morosidad (alrededor de 0,05) y el promedio de evaluaciones (cerca de 0,01). Las demás variables muestran cambios pequeños en esta métrica. La consistencia del patrón entre entrenamiento y prueba respalda que estas variables son informativas para este modelo, pero no establece que causen la deserción.

![Importancia de las variables por permutación en entrenamiento y prueba](../images/permutation_feature_importance.png)
Figura 6. *Disminución del F1-macro tras permutar cada predictor.* Los paneles corresponden a entrenamiento y prueba; una disminución mayor indica mayor contribución predictiva en este modelo, no un efecto causal.


## Discusión

En respuesta a la pregunta del estudio, el mejor resultado fue de Gradient Boosting: F1-macro de 0,783 en la clasificación multiclase y de 0,940 en la binaria (Tablas 5 y 7). La matriz de confusión (Tabla 6) muestra un rendimiento desigual: el modelo identifica mejor a graduados y desertores que a estudiantes en curso. En la tarea binaria, SVM obtuvo un resultado casi idéntico al de Gradient Boosting, por lo que no se observa una ventaja práctica clara entre ambos. En el modelo logístico explicativo, la importancia por permutación (Figura 6) y los coeficientes (Tabla 8) destacan el índice de rendimiento académico y la morosidad.

El aporte principal es identificar, para esta muestra concreta, qué señales del primer año permiten distinguir mejor los estados académicos. La importancia del rendimiento es compatible con los enfoques de integración académica de Tinto (1975, 1993); a su vez, las asociaciones de morosidad y becas concuerdan con modelos que consideran factores individuales y contextuales (Bean, 1980; Bean y Metzner, 1985; Yorke y Longden, 2004). El buen desempeño binario podría deberse a que las variables académicas de ambos semestres resumen el progreso alcanzado al cierre del año, pero por esa misma razón el resultado no demuestra que sea posible anticipar la deserción al momento de la inscripción. La superposición entre grupos y los errores de la Tabla 6 confirman que las categorías no se explican solo mediante las variables numéricas seleccionadas.

En términos prácticos, estos modelos podrían servir como apoyo para orientar el contacto y el acompañamiento de estudiantes al cierre del primer año, no para etiquetarlos ni restringir oportunidades. La tarea binaria solo distingue graduados y desertores y excluye a quienes continúan en curso; por ello, no predice la situación de esa categoría.

Los resultados tienen varias limitaciones. El conjunto es observacional y su proceso de selección y representatividad no está documentado; pueden faltar factores institucionales, personales y socioeconómicos relevantes, y no se realizó validación externa ni temporal. En este informe no se presentan métricas complementarias como precisión, *recall* o AUC, que ayudarían a valorar distintos costos de error. La escala original de las variables numéricas se conservó en los modelos comparativos, lo que puede afectar especialmente a SVM, K-NN y modelos regularizados; además, la curva de complejidad utiliza repetidamente el conjunto de prueba. Finalmente, la importancia y los coeficientes se estimaron en un modelo logístico reducido y no deben confundirse con explicaciones causales ni atribuirse directamente al modelo Gradient Boosting de mejor F1.

## Conclusión

En función de los resultados, Gradient Boosting fue el modelo con mayor F1-macro tanto en la clasificación multiclase (0,783) como en la binaria (0,940). En el modelo logístico explicativo, el índice de rendimiento académico y la morosidad fueron los predictores con mayor contribución a la clasificación, seguidos por el promedio de evaluaciones. En conjunto, los hallazgos indican que la información académica del primer año permite distinguir graduados y desertores con un F1-macro alto dentro de esta muestra, pero la categoría en curso es más difícil de identificar. La evidencia es prometedora como apoyo para orientar acciones de acompañamiento, aunque se requieren validación externa, métricas complementarias y controles metodológicos adicionales antes de cualquier implementación institucional.

## Bibliografía

Bean, J. P. (1980). Dropouts and turnover: The synthesis and test of a causal model of student attrition. *Research in Higher Education, 12*(2), 155-187.

Bean, J. P., y Metzner, B. S. (1985). A conceptual model of nontraditional undergraduate student attrition. *Review of Educational Research, 55*(4), 485-540.

OECD. (2019). *Education at a Glance 2019: OECD Indicators*. OECD Publishing.

Tinto, V. (1975). Dropout from higher education: A theoretical synthesis of recent research. *Review of Educational Research, 45*(1), 89-125.

Tinto, V. (1993). *Leaving College: Rethinking the Causes and Cures of Student Attrition* (2nd ed.). University of Chicago Press.

Yorke, M., y Longden, B. (2004). *Retention and Student Success in Higher Education*. Society for Research into Higher Education y Open University Press.

