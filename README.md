# IT Support Ticket Analisis con Python
## Objetivo
Analizar tickets de soporte técnico para detectar patrones de volumen, prioridad, canales, tiempos de respuesta/resolución y satisfacción del cliente.

## Dataset
Fuente: Kaggle - Customer Support Ticket Dataset
Link: (https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset)

## Preguntas de análisis
1. ¿Qué tipos de tickets son más frecuentes?
2. ¿Qué prioridades tardan más en resolverse?
3. ¿Qué canales concentran más tickets?
4. ¿Cómo se relaciona el tiempo de resolución con la satisfacción?
5. ¿Qué productos generan más tickets?

## Pipeline
1. Carga del CSV.
2. Exploración inicial.
3. Limpieza de columnas, nulos, duplicados y categorías.
4. Creación de features.
5. Visualizaciones.
6. Exportación del dataset limpio.

## Hallazgos principales
- Insight 1: ...
- Insight 2: ...
- Insight 3: ...

## Cómo ejecutar
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
jupyter notebook notebooks/eda.ipynb