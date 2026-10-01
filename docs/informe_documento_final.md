**Trabajo Práctico 1 - Aprendizaje Automático**  
**Estudiante:** Diego Rojas  
**Tema:** Determinantes de la deserción universitaria y predicción

## Resumen

> **Completar al finalizar el análisis.** Presentar en un máximo de 200 palabras: el problema estudiado, los datos utilizados, los modelos comparados, el resultado principal y la conclusión más importante. No incluir información que no se desarrolle posteriormente en el informe.

## Introducción

Este trabajo analiza los determinantes más importantes de la deserción universitaria y desarrolla un modelo predictivo para estimar el riesgo de abandono de los estudiantes al finalizar su primer año. Identificar este riesgo y las variables de mayor impacto resulta fundamental para que áreas como Bienestar Estudiantil o Secretaría Académica puedan realizar intervenciones directas e informadas.

La literatura teórica (Tinto, 1975, 1993; Bean, 1980) y empírica (Yorke y Longden, 2004; OECD, 2019) muestra que la deserción es un fenómeno multicausal, determinado por la interacción de factores individuales, institucionales, socioeconómicos y de integración académica. Debido a que la relevancia de estas variables varía según el contexto, este estudio busca evaluar qué factores resultan más informativos en el conjunto de datos analizado.

Para responder a la pregunta central **¿qué variables permiten explicar y predecir mejor la deserción universitaria después del primer año?**, se realizará un análisis exploratorio y se estructurará la modelado en dos etapas: una clasificación multiclase (graduados, desertores y en curso) y una binaria (graduados vs. desertores). Evaluando los modelos mediante el *F1-score*, se espera confirmar que el desempeño académico inicial, la situación financiera (deuda y becas), la edad y la modalidad de ingreso se posicionen entre los predictores más determinantes.

## Materiales y métodos

Usamos la totalidad del dataset universitario (50k lineas). Las variables fueron renombradas usando la metedologia de *lower_snake_case*. Además, muchas variables catégoricas fueron transformadas a booleanas para facilitar su análsis y posterior uso en los algoritmos. Tambien, se crearon nuevas variables númericas realizando promedios o ratios con las variables existentes.

### i) Datos y variables explicativas (E)

El dataset original contiene 50 mil líneas y 27 variables. Al analizar tanto las variables númericas como categóricas podemos apreciar de que no existen valores nulos en el dataset. Otro punto importante es que para las variables númericas que representan la edad, puntajes, unidades créditicias, etc. no presentan valores negativos, lo cual esta asociado con la lógica esperada. En la tabla 1 y 2 se puede ver con más detalle los principales descriptivos de las principales variables que vamos a usar más adelante.

Tabla 1. *Resumen descriptivo de las variables númericas del dataset ($N = 50.000$)*

| Variable | $N$ | Miss | Missing (%) | Zeros | Positivos | Negativos | Min | Max | Mean | $p_{0.01}$ | $p_{0.05}$ | $p_{0.25}$ | $p_{0.50}$ | $p_{0.75}$ | $p_{0.95}$ | $p_{0.99}$ | Std | Coeff of Variation |
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

<small>Resumen de estadísticos descriptivos, distribuciones de percentiles y proporciones de valores nulos/ceros para la cohorte analizada. $N$ = Tamaño de la muestra (número total de registros); Miss = Cantidad de datos faltantes; Missing (%) = Porcentaje de datos faltantes; Zeros = Cantidad de valores iguales a cero; Positivos / Negativos = Frecuencia de valores estrictamente mayores o menores a cero; Min / Max = Valor mínimo y máximo observado; Mean = Media aritmética; $p_{0.01}, p_{0.05}, \dots, p_{0.99}$ = Percentiles específicos del 1 %, 5 %, 25 % (primer cuartil), 50 % (mediana), 75 % (tercer cuartil), 95 % y 99 %; Std = Desviación estándar; Coeff of Variation = Coeficiente de variación (Std / Mean); uc = Unidades curriculares.</small>

Incluir gráfico de correlación y boxplot

Tabla 2. *Resumen descriptivo de las variables categóricas del modelo ($N = 50.000$)*

| Variable | Missing | Niveles | Moda | Frec_Moda | Largo |
| :--- | :---: | :---: | :--- | :---: | :---: |
| **Estudios_máximos_antes_de_la_inscripción** | 0 | 5 | Educación Secundaria | 43.950 | 50.000 |
| **estado_civil** | 0 | 6 | Soltero | 45.861 | 50.000 |
| **modo_aplicacion** | 0 | 4 | Acceso General | 34.694 | 50.000 |
| **macro_categoria_carrera** | 0 | 6 | Comunicación, marketing y diseño | 12.490 | 50.000 |

<small>Resumen de propiedades para las variables cualitativas y categóricas del conjunto de datos. Variable = Nombre del atributo analizado; Missing = Cantidad de datos faltantes; Niveles = Número de categorías únicas o distintas de la variable; Moda = Categoría con mayor frecuencia de aparición; Frec_Moda = Frecuencia absoluta (número de casos) correspondientes a la moda; Largo = Total de registros evaluados ($N$).</small>


### ii) Variable respuesta y tarea objetivo (T)

La variable respuesta es `target`, con tres estados: **Graduado**, **Desertor** y **En curso**. Para la tarea multiclase se conservarán las tres categorías. Para la tarea binaria se excluirá temporalmente la categoría **En curso** y se clasificarán únicamente los casos **Graduado** y **Desertor**, de acuerdo con el objetivo de estimar el riesgo de deserción una vez finalizado el primer año.

Las etiquetas fueron tipificadas de la siguiente manera:
  - Graduado igual a 0
  - Desertor igual a 1
  - En Curso igual a 2

La tabla 3 muestra la distribución de la variable objetivo. Podemos notar que no hay un desbalanceo llamativo en ninguna categoría y que la tasa de graduados es casi del 50%.

Tabla 3. *Distribución de frecuencias de la variable objetivo (target) ($N = 50.000$)*

| Variable | Frecuencia | Frecuencia relativa (%) |
| :--- | :---: | :---: |
| **Graduado** | 23.707 | 47,41 % |
| **Desertor** | 16.529 | 33,06 % |
| **En Curso** | 9.764 | 19,53 % |

<small>Distribución de categorías de la variable dependiente u objetivo (target) del estudio. Variable = Estado académico final del estudiante; Frecuencia = Número absoluto de estudiantes en cada categoría; Frecuencia relativa (%) = Porcentaje respecto al total de la muestra analizada ($N = 50.000$).</small>

Incluir IV 

### iii) Manejo de datos y esquemas de clasificación

Para ambos modelos se separa el dataset en train y test (80/20) estratificando por la variable obtivo. Además, se utilizará exclusivamente el **F1-score** para evaluar y comparar los modelos, tanto en la tarea binaria como en la multiclase. Esta decisión se fundamenta en que esta métrica es mucho mas robusta cuando hay presencia de desbalance.

#### Clasificación multiclase

Describir la nueva separación de los datos y la estrategia utilizada para extender cada modelo al problema multiclase, por ejemplo one-vs-rest u one-vs-one. Indicar los hiperparámetros evaluados para K-NN y árboles de decisión, el número de particiones de la validación cruzada y los valores finalmente seleccionados.

### Evaluación de modelos


| Modelo | Estrategia multiclase | Hiperparámetros y rangos evaluados | Valores finales |
| :---- | :---- | :---- | :---- |
| K-NN | **Completar** | **Completar** | **Completar** |
| Árbol de decisión | **Completar** | **Completar** | **Completar** |
| Boosting | **Completar** | **Completar** | **Completar** |
| Bagging / Random Forest | **Completar** | **Completar** | **Completar** |


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

