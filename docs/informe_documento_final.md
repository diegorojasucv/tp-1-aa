**Trabajo Práctico 1 - Aprendizaje Automático**  
**Estudiante:** Diego Rojas  
**Tema:** Determinantes de la deserción universitaria y predicción

## Resumen

> **Completar al finalizar el análisis.** Presentar en un máximo de 200 palabras: el problema estudiado, los datos utilizados, los modelos comparados, el resultado principal y la conclusión más importante. No incluir información que no se desarrolle posteriormente en el informe.

## Introducción

La deserción universitaria constituye un problema relevante para las instituciones de educación superior porque afecta las trayectorias educativas de los estudiantes y también implica costos académicos, sociales y económicos. En este trabajo se estudia la deserción luego del primer año universitario, con el propósito de identificar los factores asociados con la permanencia, la graduación y el abandono, y de construir una herramienta que permita estimar tempranamente el riesgo de deserción. En particular, se analizará si las características sociodemográficas y de admisión, la situación económica y administrativa, y el desempeño académico temprano permiten distinguir entre estudiantes graduados, desertores y estudiantes que continúan en curso.

La literatura sobre permanencia estudiantil señala que la deserción no suele explicarse por un único factor, sino por la interacción entre características individuales, condiciones institucionales, integración académica y social, y restricciones económicas. El modelo de integración de Tinto (1975, 1993) destaca el papel de la integración académica y social en la persistencia; los modelos de Bean (1980) y Bean y Metzner (1985) incorporan, además, la influencia de factores externos y de las condiciones de los estudiantes no tradicionales. Estudios empíricos también han asociado la deserción con el rendimiento académico inicial, la asistencia, la situación financiera, la edad, la modalidad de ingreso y las características del programa de estudios (Yorke y Longden, 2004; OECD, 2019). Sin embargo, la importancia relativa de estos determinantes puede variar entre instituciones, países y cohortes. Por ello, este análisis busca complementar la evidencia general con una comparación de modelos aplicada al conjunto de datos disponible, identificando qué variables resultan más informativas en este caso y qué capacidad predictiva alcanzan los modelos.

La pregunta principal es: **¿qué variables permiten explicar y predecir mejor la deserción universitaria después del primer año?** Para responderla, primero se realizará un análisis exploratorio de las variables y de la distribución de las tres categorías de la variable de respuesta: estudiantes graduados, desertores y estudiantes en curso. Luego se abordará una tarea multiclase para comparar estos grupos y, en una segunda etapa, una tarea binaria que considere únicamente graduados y desertores, con el objetivo de estimar el riesgo de deserción. Se compararán distintas familias de modelos utilizando exclusivamente el F1-score como métrica de evaluación y criterio de selección, y se analizará la importancia de los atributos. Se plantea como hipótesis que el desempeño académico del primer año, las notas, la situación de matrícula y deuda, la beca, la edad y algunas características de ingreso estarán entre los predictores más relevantes. El resto del informe presenta los materiales y métodos, los resultados, la discusión, las conclusiones y la bibliografía.

## Materiales y métodos

### i) Datos y variables explicativas (E)

> **Completar con la información documentada en el análisis.** Describir la fuente del conjunto de datos, el período o cohorte representada, el número de observaciones y la cantidad de variables. Indicar los criterios de inclusión y exclusión, los valores faltantes, los posibles errores de medición y los sesgos de selección que puedan afectar la generalización.

Las variables explicativas se organizarán en los siguientes grupos:

- **Características personales y sociodemográficas:** edad al momento de la inscripción, sexo, estado civil, condición de estudiante internacional y necesidades educativas especiales.
- **Antecedentes y admisión:** nivel máximo de estudios previo, puntaje del examen de ingreso, modalidad de aplicación, carrera y condición de desplazamiento.
- **Situación económica y administrativa:** deuda, pago de matrícula al día, posesión de beca, ingresos de los padres y demanda cognitiva de los padres.
- **Desempeño académico temprano:** unidades inscriptas, cantidad de evaluaciones, unidades aprobadas y nota promedio durante el primer y segundo semestre.

Describir el balance de clases mediante una tabla y especificar cómo se tratará el eventual desbalance: ponderación de clases, muestreo u otra estrategia. Aclarar qué transformaciones se aplicaron a las variables categóricas y numéricas, y cómo se evitó que información del conjunto de prueba interviniera en el entrenamiento.

### ii) Variable respuesta y tarea objetivo (T)

La variable respuesta es `target`, con tres estados: **Graduado**, **Desertor** y **En curso**. Para la tarea multiclase se conservarán las tres categorías. Para la tarea binaria se excluirá temporalmente la categoría **En curso** y se clasificarán únicamente los casos **Graduado** y **Desertor**, de acuerdo con el objetivo de estimar el riesgo de deserción una vez finalizado el primer año.

> **Completar:** indicar cómo se codificaron las etiquetas, qué clase se definió como evento positivo en la tarea binaria y cuántos casos quedaron disponibles después de esa selección.

### iii) Manejo de datos y esquemas de clasificación

#### Clasificación multiclase

Describir la nueva separación de los datos y la estrategia utilizada para extender cada modelo al problema multiclase, por ejemplo one-vs-rest u one-vs-one. Indicar los hiperparámetros evaluados para K-NN y árboles de decisión, el número de particiones de la validación cruzada y los valores finalmente seleccionados.

| Modelo | Estrategia multiclase | Hiperparámetros y rangos evaluados | Valores finales |
| :---- | :---- | :---- | :---- |
| K-NN | **Completar** | **Completar** | **Completar** |
| Árbol de decisión | **Completar** | **Completar** | **Completar** |
| Boosting | **Completar** | **Completar** | **Completar** |
| Bagging / Random Forest | **Completar** | **Completar** | **Completar** |

#### Clasificación binaria

Describir la separación entre entrenamiento y prueba, indicando proporciones, semilla aleatoria y si se utilizó estratificación. Se entrenarán y compararán regresión logística, máquinas de soporte vectorial y árboles de decisión. Luego se incorporará un ensamble por Voting, si corresponde al análisis realizado.

Para cada modelo, completar la siguiente información:

| Modelo | Hiperparámetros y rangos evaluados | Criterio de selección | Valores finales |
| :---- | :---- | :---- | :---- |
| Regresión logística | **Completar** | Validación cruzada: **completar** | **Completar** |
| SVM | **Completar** | Validación cruzada: **completar** | **Completar** |
| Árbol de decisión | **Completar** | Validación cruzada: **completar** | **Completar** |
| Voting | **Completar** | **Completar** | **Completar** |

### Evaluación de modelos

Se utilizará exclusivamente el **F1-score** para evaluar y comparar los modelos, tanto en la tarea binaria como en la multiclase. Esta decisión se fundamenta en que el conjunto de datos puede presentar un desbalance entre categorías: una predicción que favorezca a la clase mayoritaria podría obtener una accuracy aparentemente alta sin detectar adecuadamente a los estudiantes desertores. El F1-score combina precisión y recall mediante su media armónica:

$$F_1 = 2 \cdot \frac{\mathrm{precisión} \cdot \mathrm{recall}}{\mathrm{precisión} + \mathrm{recall}}$$

Por lo tanto, el valor sólo será alto cuando el modelo mantenga simultáneamente un nivel adecuado de aciertos entre las predicciones positivas y de detección de los casos positivos. La media armónica penaliza los valores bajos: un modelo no podrá compensar un recall deficiente con una precisión elevada, o viceversa. Esto resulta especialmente relevante en la tarea binaria, donde el objetivo es detectar desertores sin generar un número excesivo de falsas alarmas. En la tarea multiclase se utilizará el **F1 macro**, que calcula el F1-score de cada clase y luego les asigna el mismo peso, evitando que la clase más frecuente domine la evaluación.

El modelo final se seleccionará según el mayor F1-score obtenido en el conjunto de prueba, o según el mayor F1 macro en la tarea multiclase. Para reducir el riesgo de elegir un modelo por una partición favorable, la selección de hiperparámetros deberá realizarse exclusivamente dentro del conjunto de entrenamiento mediante validación cruzada. El F1-score no informa sobre calibración de probabilidades ni incorpora costos diferenciados para cada tipo de error; por eso, sus resultados se interpretarán junto con la matriz de confusión cuando esté disponible. Además, la importancia de una variable se entenderá como capacidad predictiva dentro del modelo y no como evidencia de una relación causal.

## Resultados

> **Completar con los resultados del análisis.** Esta sección debe responder cuáles fueron los hallazgos, sin interpretar en profundidad sus causas.

### Análisis exploratorio

Presentar la distribución de la variable respuesta, las variables con valores faltantes y las principales relaciones observadas. Incorporar la **Tabla 1** y las **Figuras 1-__**, citándolas explícitamente en el texto.

**Tabla 1.** Distribución de las clases de la variable respuesta.

| Clase | Frecuencia | Porcentaje |
| :---- | ----: | ----: |
| Graduado | **Completar** | **Completar** |
| Desertor | **Completar** | **Completar** |
| En curso | **Completar** | **Completar** |

Descripción: frecuencia y porcentaje de cada categoría de `target`. Completar las siglas utilizadas.

### Desempeño de la clasificación binaria

Describir y comparar los modelos binarios mediante la **Tabla 2** y las figuras correspondientes. Informar qué modelo alcanzó el mejor F1-score en test. La precisión y el recall se utilizarán únicamente para explicar la composición del F1-score si se decide incluirlos en una matriz de confusión o en el texto metodológico, pero no serán métricas adicionales de selección.

**Tabla 2.** Desempeño de los modelos de clasificación binaria en el conjunto de prueba.

| Modelo | F1-score |
| :---- | ----: |
| Regresión logística | **Completar** |
| SVM | **Completar** |
| Árbol de decisión | **Completar** |
| Voting | **Completar** |

### Desempeño de la clasificación multiclase

Reportar el F1-score de cada clase y el F1 macro. Explicar qué clases son más difíciles de distinguir y qué errores aparecen con mayor frecuencia. El promedio macro será el valor principal porque asigna la misma importancia a Graduado, Desertor y En curso, independientemente de sus frecuencias.

**Tabla 3.** Desempeño de los modelos de clasificación multiclase.

| Modelo | F1 macro |
| :---- | ----: |
| K-NN | **Completar** |
| Árbol de decisión | **Completar** |
| Boosting | **Completar** |
| Bagging / Random Forest | **Completar** |

### Curvas de complejidad e importancia de atributos

Mostrar cómo cambia el desempeño en entrenamiento y prueba al variar los hiperparámetros principales. Describir si aparece sobreajuste o subajuste y relacionarlo con la capacidad de generalización. Presentar la importancia de atributos o una medida equivalente, aclarando el método utilizado.

**Figura __.** Curva de complejidad del modelo **[completar]**.

Descripción: desempeño en entrenamiento y prueba en función de **[hiperparámetro]**. Completar las siglas y unidades.

**Figura __.** Variables más influyentes para la predicción de **[tarea]**.

Descripción: importancia estimada mediante **[método]**. La importancia se interpreta como capacidad predictiva dentro del modelo y no como efecto causal.

## Discusión

Los resultados principales indican que **[completar modelo y F1-score]** fue el modelo con mejor desempeño para **[tarea]**. La variable o grupo de variables más informativo fue **[completar]**, lo que permite responder parcialmente la pregunta planteada en la introducción. La elección se fundamenta en el mayor F1-score, ya que esta métrica exige un equilibrio entre detectar correctamente los casos relevantes y evitar predicciones positivas incorrectas.

La relevancia observada del desempeño académico temprano, la situación económica o administrativa y las características de admisión debe discutirse en relación con los modelos de permanencia de Tinto (1975, 1993), Bean (1980) y Bean y Metzner (1985), así como con la evidencia sintetizada por Yorke y Longden (2004) y OECD (2019). Indicar si los hallazgos coinciden con esa literatura o si aparecen diferencias atribuibles al contexto, la cohorte o la composición de la muestra.

Comparar el desempeño de los modelos y explicar las diferencias en términos de complejidad, supuestos, sensibilidad al desbalance y capacidad de generalización. Discutir las aplicaciones prácticas de un sistema de alerta temprana, aclarando que un puntaje predictivo debería orientar intervenciones de acompañamiento y no utilizarse como criterio automático de exclusión.

Finalmente, señalar las limitaciones: **[completar según el análisis]**. Considerar la naturaleza observacional de los datos, la posible falta de variables institucionales o socioeconómicas, el hecho de que asociación no implica causalidad, la calidad y representatividad de la muestra, y la ausencia de validación externa o temporal si corresponde.

## Conclusión

En base a los resultados obtenidos, **[modelo seleccionado]**, con un F1-score de **[completar]**, permite resolver **[confiable/moderadamente/limitadamente]** la tarea de **[clasificación binaria o multiclase]** a partir de las variables disponibles. Los predictores más informativos fueron **[completar]**. El F1-score fue elegido porque ofrece un criterio equilibrado frente al desbalance de clases y evita seleccionar un modelo que funcione bien sólo para la clase mayoritaria. Estos resultados sugieren que **[implicancia principal]**, aunque su aplicación debe considerar las limitaciones del conjunto de datos y utilizarse como apoyo para intervenciones educativas, no como sustituto del análisis institucional o del acompañamiento individual.

## Bibliografía

Bean, J. P. (1980). Dropouts and turnover: The synthesis and test of a causal model of student attrition. *Research in Higher Education, 12*(2), 155-187.

Bean, J. P., y Metzner, B. S. (1985). A conceptual model of nontraditional undergraduate student attrition. *Review of Educational Research, 55*(4), 485-540.

OECD. (2019). *Education at a Glance 2019: OECD Indicators*. OECD Publishing.

Tinto, V. (1975). Dropout from higher education: A theoretical synthesis of recent research. *Review of Educational Research, 45*(1), 89-125.

Tinto, V. (1993). *Leaving College: Rethinking the Causes and Cures of Student Attrition* (2nd ed.). University of Chicago Press.

Yorke, M., y Longden, B. (2004). *Retention and Student Success in Higher Education*. Society for Research into Higher Education y Open University Press.

