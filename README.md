# Predicción de Ventas para Supermercado con Power BI y Python

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-orange.svg)](https://powerbi.microsoft.com/desktop/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


## Descripción del Proyecto

Este proyecto se centra en la predicción de las ventas de un supermercado mediante el uso de técnicas de aprendizaje automático en Python y la visualización de los resultados y el rendimiento del modelo a través de un dashboard interactivo creado con Power BI. El análisis abarca la exploración de datos históricos de ventas, la construcción y evaluación de un modelo predictivo, y la presentación de insights clave sobre las ventas y la precisión del modelo.

## Contenido del Repositorio

El repositorio contiene los siguientes archivos y carpetas:

* `data/`: Contiene los archivos de datos.
* `models/`: Contiene los modelos serializados.
* `output/`: Contiene los archivos de salida (datos_limpios.csv, predicciones.csv).
* `src/`: Contiene el código fuente de Python.
* `test/`: Contiene los archivos de prueba.
* `generacionDatos.py`: Script para generar datos.
* `README.md`: Este archivo.
* `requirements.txt`: Lista de librerías de Python necesarias.
* `LICENSE`: Archivo de licencia (ej. MIT).

## Tecnologías Utilizadas

* **Python:** Lenguaje de programación utilizado para la manipulación de datos, el entrenamiento del modelo de machine learning y la generación de predicciones.
* **Librerías de Python:**
    * Pandas: Para la manipulación y análisis de datos.
    * NumPy: Para operaciones numéricas.
    * Scikit-learn: Para la construcción y evaluación del modelo de machine learning.
    * Unittest: Para los test de prueba
    * Matplotlib: Para los gráficos
    * JobLin: Para la persistencia del modelo
    * Os y System: Para el sistema de rutas
      
* **Power BI Desktop:** Herramienta de inteligencia empresarial utilizada para la creación del dashboard interactivo.
* **Git:** Sistema de control de versiones utilizado para la gestión del repositorio.
* **GitHub:** Plataforma para el alojamiento del repositorio y la colaboración.

## Estructura del Dashboard de Power BI

El dashboard de Power BI consta de las siguientes páginas:

1.  **Página Principal:**
    * KPIs clave del rendimiento del modelo (R-cuadrado, MAE, RMSE, MAPE) con formato condicional.
    * Comparación visual de las ventas reales vs. las ventas predichas a lo largo del tiempo.
    * Gráfico de dispersión de las ventas predichas en función de las ventas reales.
    * Breve resumen del rendimiento del modelo.
    * Botón de navegación a la página de "Análisis de Ventas".

2.  **Análisis de Ventas:**
    * Tendencia de ventas diarias segmentada por estado de promoción ("Sí hay promoción", "No hay promoción").
    * Distribución de las ventas por categoría de producto.
    * Comparativa de las ventas por ubicación de la tienda.
    * Análisis de la distribución de ventas por día festivo.
    *  * Botón de navegación a la página de "Análisis de de Residuos".
3.  **Análisis de Residuos del Modelo:**
    * Tendencia de los residuos (errores de predicción) a lo largo del tiempo.
    * Métricas resumen de los residuos (media y desviación estándar).
    * Distribución de la frecuencia de los residuos (histograma).

## Posibles Mejoras Futuras

* Implementar técnicas de ingeniería de características más avanzadas.
* Experimentar con diferentes algoritmos de machine learning.
* Incorporar datos externos (ej., datos económicos, eventos).
* Crear un modelo de predicción en tiempo real.
* Publicar el dashboard de Power BI en la nube para acceso compartido.
* Añadir más interactividad al dashboard.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Iván
www.linkedin.com/in/ivandelllanoblanco


---

¡Gracias por explorar este proyecto! Espero que sea de utilidad y no dudes en contactarme para posibles mejoras.
