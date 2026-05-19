# IT Support Ticket Analisis con Python
## Objetivo
Analizar tickets de soporte técnico para detectar patrones de volumen, prioridad, canales, tiempos de respuesta/resolución y satisfacción del cliente.

## Dataset
Fuente: Kaggle - Customer Support Ticket Dataset
Link: (https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset)

## Preguntas de análisis

1. ¿Qué tipos de tickets son más frecuentes?
2. ¿Cómo se distribuyen los tickets según prioridad?
3. ¿Los tickets críticos tardan más o menos en resolverse?
4. ¿Qué canal de soporte tiene mejor satisfacción promedio?
5. ¿Los tiempos de resolución más largos se asocian con menor satisfacción del cliente?
6. ¿Qué productos generan mayor carga de soporte?

## Pipeline

1. **Carga del dataset original** desde `data/raw/customer_support_tickets.csv`.
2. **Validación inicial** del dataset para comprobar columnas requeridas, número de filas y estructura general.
3. **Exploración inicial** con revisión de tipos de datos, valores nulos, duplicados y estadísticas descriptivas.
4. **Limpieza de datos**, incluyendo:
   - conversión de nombres de columnas a `snake_case`;
   - eliminación de columnas con información personal o texto libre de alto ruido;
   - conversión de fechas;
   - conversión de variables numéricas;
   - normalización de categorías;
   - eliminación de duplicados.
5. **Creación de features analíticas**, incluyendo:
   - `product_age_days`;
   - `resolution_hours`;
   - `has_negative_resolution_time`;
   - `has_resolution`;
   - `satisfaction_group`;
   - `is_high_priority`;
   - variables temporales derivadas de `first_response_time`.
6. **Análisis exploratorio** de variables numéricas y categóricas.
7. **Generación de visualizaciones** para analizar volumen, prioridad, canal, satisfacción, tiempos de resolución y productos con más tickets.
8. **Exportación del dataset procesado** a `data/processed/clean_customer_support_tickets.csv`.
9. **Exportación de gráficos** a `reports/figures/`.

## Hallazgos principales

- El dataset contiene **8.469 tickets de soporte**, lo que permite analizar patrones operativos con un volumen suficiente de datos.
- El tipo de ticket más frecuente fue **Refund Request**, con **1.752 tickets**, lo que indica una carga importante relacionada con solicitudes de devolución.
- La prioridad más frecuente fue **Medium**, con **2.192 tickets**, lo que sugiere que la mayor parte de la operación se concentra en incidencias de prioridad intermedia.
- El canal con mayor volumen fue **Email**, con **2.143 tickets**, por lo que representa uno de los canales principales de entrada para soporte.
- El producto con mayor número de tickets fue **Canon EOS**, con **240 tickets**, lo que puede indicar alta demanda de soporte, mayor volumen de usuarios o mayor complejidad del producto.
- La satisfacción promedio fue de **2.99 sobre 5**, lo que muestra una experiencia de cliente intermedia y deja espacio para mejoras en el proceso de soporte.
- La mediana del tiempo válido de resolución fue de **6.34 horas**, considerando solo tickets con tiempos de resolución válidos.
- Se detectaron **1.365 casos con inconsistencias temporales**, donde `time_to_resolution` era anterior a `first_response_time`. Estos casos fueron marcados con `has_negative_resolution_time` y excluidos del cálculo válido de `resolution_hours`.
- El análisis muestra que antes de sacar conclusiones sobre tiempos de resolución es fundamental validar la calidad de los datos, especialmente cuando se trabaja con fechas operativas.

## Cómo ejecutar
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
jupyter notebook notebooks/eda.ipynb