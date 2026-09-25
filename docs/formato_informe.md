# **Aprendizaje Automático**

## **Trabajo práctico 1**

### **Contexto y objetivo**

### En este TP se trabajará con datos sobre deserción de estudiantes universitarios. El conjunto de datos describe la situación de una institución de educación superior y está relacionado con estudiantes matriculados en diferentes carreras (química, diseño, educación, ingeniería, periodismo, economía, etc). Los datos incluyen información disponible al momento de la inscripción del estudiante y el rendimiento académico durante el primer año.

### El **objetivo principal** es construir modelos de clasificación para predecir la deserción de los estudiantes. Para ello deberán implementar, comparar y analizar distintos modelos clásicos de aprendizaje automático, utilizando métricas adecuadas y curvas de complejidad para evaluar el desempeño y la capacidad de generalización de cada modelo.

Se evaluará en el informe que el mismo refleje la incorporación de herramientas y conceptos relativos específicamente a la materia. Entre otras cosas, que muestre cierta reflexión acerca de las propiedades de los modelos utilizados para abordar el problema, sus particularidades, supuestos y limitaciones, y su capacidad de generalización.

### El trabajo será grupal (3–4 integrantes). Todos deben conocer el desarrollo del trabajo, ya que podrá ser evaluado también en el examen final. 

### Lo que van a encontrar a continuación es una guía orientativa que pueden usar como referencia al redactar sus informes. No es un manual ni la única forma correcta de hacerlo, así que no lo tomen como una obligación. La guía resalta las cosas que nos gustaría ver y valoramos en los informes. Tomenla simplemente como una ayuda para orientar la redacción y el trabajo.

### **Fecha límite de entrega:** Dmingo 11 de Octubre de 2026 a las 23:59. 

### 

### **Formato del informe:**

### **Trabajo práctico X: \*\*\*\*\***

## **Tema tratado en los datos**  **Nombre estudiantes**  **Extensión máxima del TP: 12 carillas**

### **Resumen** del estilo de un artículo científico de no más de 200 palabras

### **Introducción**

## Máximo 1 carilla o 3 párrafos. Aquí deben contestar la pregunta: **¿Qué problema se estudió?**

* ## **Párrafo 1** Se recomienda estructurarlo en tres frases: 

  * ## **Frase 1**: referencia general a la relevancia del tema, conectada con el problema de estudio. 

  * ## **Frase 2**: especificar con claridad qué se va a analizar o qué pregunta se busca contestar (¿Qué variables esperan que sean relevantes? ¿Por qué?) 

  * ## **Frase 3**: resumir brevemente cómo se abordará el problema. 

* ## **Párrafo 2** Extender las frases 1 y 2 del párrafo anterior con una breve revisión bibliográfica, señalando el *gap* que el análisis busca cubrir o el problema concreto a resolver. Este párrafo debe servir de fundamento para la pregunta planteada, sin desviarse hacia otros temas. Concluir indicando de qué manera el planteo o análisis permitirá responder a la pregunta. 

* ## **Párrafo 3** Reafirmar la pregunta que el análisis busca contestar, explicitar cómo se abordará y formular las hipótesis. Este párrafo debe incluir el **objetivo del trabajo** y explicar la **organización del resto del documento**. 

### **Materiales y métodos**

## Aquí deben contestar la pregunta: **¿Cómo se estudió el problema?**

## Explicar qué datos se usaron, cómo fueron tomados y cómo se analizaron. Esta sección tendrá tres subsecciones:

### **i) Datos / Variables explicativas (E)**

Describir la conformación de la muestra: fuente, número de casos, características, criterios de calidad y posibles sesgos. Realizar un análisis breve de los atributos disponibles para la predicción, manteniendo la descripción clara y concisa, evitando tablas extensas o información innecesaria. Detallar el balance de clases y, en caso de existir desbalance, indicar la estrategia que se empleará para tenerlo en cuenta durante el análisis.

### **ii) Variable respuesta / Tarea objetivo (T)**

Explicar cómo se manejaron los datos de la variable de salida y cómo se generaron las etiquetas. Si la variable proviene de un procedimiento particular, detallar el método utilizado en esta sección.

### **iii) Manejo de datos y esquemas de clasificación**

#### **Clasificación binaria**

Se realizará inicialmente un esquema de clasificación binaria, separando los datos en conjuntos de entrenamiento y prueba (train/test). Aquí se detallan las proporciones usadas. Se entrenarán modelos clásicos como regresión logística, máquinas de soporte vectorial (SVM) y árboles de decisión. Los resultados de estos modelos se compararán entre sí en la sección de resultados. Mientras que en métodos incluimos sólo detalles del proceso de optimización de hiper-parámetros.

Para cada modelo deben **indicar explícitamente los hiper-parámetros considerados** (con sus rangos) y los valores finales seleccionados, explicando el criterio de selección (por ejemplo, mediante validación cruzada). Esta información se podrá resumir en una tabla comparativa.

Posteriormente, se implementará un ensamble de los modelos anteriores mediante técnicas como Voting, acompañado de un análisis comparativo de desempeño. 

#### **Clasificación multiclase**

En una segunda etapa se trabajará con un esquema de clasificación multiclase. Se realizará una nueva separación de datos y se entrenarán modelos como K-NN y árboles de decisión. Deben aclarar, en los casos que corresponda, las estrategias usadas para generalizar al problema multiclase, como pueden ser one-vs-one y one-vs-rest.

Para cada modelo deben **indicar explícitamente los hiper-parámetros considerados** (con sus rangos) y los valores finales seleccionados, explicando el criterio de selección (por ejemplo, mediante validación cruzada). Esta información se podrá resumir en una tabla comparativa.

Finalmente, se incluirán ensambles basados en árboles, incorporando al menos un modelo de Boosting (por ejemplo, AdaBoost o XG Boost) y uno de Bagging (como Random Forest).

#### **Evaluación de modelos**

Deben especificar las métricas de evaluación utilizadas para comparar los modelos, dentro de las vistas en la materia (accuracy, precisión, recall, F1-score y área bajo la curva ROC o AUC).

Se trabajará íntegramente en Python, utilizando librerías y frameworks estándar para análisis estadístico y aprendizaje automático.

### **Resultados**

Aquí deben contestar la pregunta: **¿Cuáles fueron los hallazgos?**

Esta sección debe ser breve, acompañando los resultados con **gráficos apropiados** y **tablas**. Preferentemente, busquen representar de manera gráfica, siendo cuidadosos en que todo lo que está en el gráfico se entienda y sea “atractivo”, teniendo en cuenta que la visualización de resultados es una parte muy relevante y determinante en su comunicación. El texto debe resumir los hallazgos e incluir la medida de performance (P) de cada modelo para la tarea objetivo (T).

En esta sección también deben reportar las **curvas de complejidad**, mostrando cómo varía el desempeño de los modelos en función de los hiper-parámetros seleccionados, y relacionando estas curvas con la capacidad de generalización de los modelos. Identificar factores más influyentes en la deserción, basándose  en la importancia de atributos.

La redacción debe seguir una secuencia lógica vinculada a los objetivos planteados (**ver formato de tablas y figuras al final).**

### **Discusión**

Aquí deben contestar la pregunta: **¿Qué significan esos resultados?**

Extensión máxima: 1 carilla, fundamentada en la bibliografía citada en la introducción.

* **Primer párrafo**: resumir los resultados principales en relación con la pregunta inicial.

* **Párrafos siguientes**: vincular los *baches* planteados en la introducción con los hallazgos. Aquí comparar el desempeño de los distintos modelos, señalar coincidencias o discrepancias con la bibliografía, explicar implicancias teóricas y aplicaciones prácticas, y resumir las pruebas que respaldan las conclusiones. Señalar el aporte más importante y discutir a qué puede deberse ese resultado. Deben incluir las limitaciones que tiene nuestro estudio.

### **Conclusión**

Un único párrafo. Ejemplo de redacción:  
 *“En base a nuestros resultados, podemos concluir que el modelo X permite resolver de manera confiable la tarea objetivo T a partir de los datos E.”*

### **Bibliografía**

Todas las referencias citadas en el trabajo deben incluirse aquí. El formato puede ser a elección, pero debe ser **homogéneo** e incluir: autores, título, revista/fuente y año de publicación.

Se recomienda usar un gestor de referencias como **Mendeley o Zotero, pero como van a ser pocas a mano está perfecto también**.

---

### **Protocolo de reporte**

* Los valores de media y desvío estándar deben tener un número de cifras consistente (ejemplo: 5.4 ± 0.2 o 5.43 ± 0.21, según la precisión adecuada).

* Toda cifra reportada debe reflejar la precisión razonable para el estudio.

**Formato de tablas:** 

Deben tener número y título en la parte **superior.** Encabezados en columnas y filas. Debajo de la tabla debe estar una descripción de los contenidos, si hay siglas o símbolos estadísticos también su significado. Ejemplo:

*Tabla 1 Título de la Tabla*

|  | Col. 1 | Col. 2 | Performance |
| :---- | :---- | :---- | :---- |
| **Var. 1** |  |  |  |
| **Var. 2** |  |  |  |

Comparación de valores de las variables según las columnas. Valor p de un Test de T/etc. Var \= Variable; Col \= Columna

**Formato de Figuras:** 

Deben tener número y título en la parte INFERIOR. Debajo de la figura debe estar una descripción de los contenidos, si hay siglas o símbolos estadísticos también su significado.

Tanto las tablas como las figuras deben estar correctamente referenciadas en el texto, donde se debe explicar de dónde salen y qué muestran. No es adecuado poner figuras “colgadas” o que tengan información en el pie que no esté también en el cuerpo del informe, cuando se trata de resultados importantes.

