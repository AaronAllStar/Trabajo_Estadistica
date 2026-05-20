# Análisis Analítico y Auditoría de Calidad de Clientes (EDA)

Este proyecto implementa una solución integral de **Calidad de Datos y Análisis Exploratorio de Datos (EDA)** con enfoque en rigor estadístico, orientado a resolver problemas comunes de inconsistencias en bases de datos transaccionales de clientes. 

---

## ¿Qué Soluciona este Trabajo?

### 1. Inconsistencias de Calidad de Datos (Data Quality)
En el origen de datos original (`clientes_dirty_semana2.csv`) existían múltiples fricciones que distorsionaban el análisis de negocio. Este pipeline las soluciona mediante reglas de calidad programáticas en Python:
*   **Errores de Geocodificación Cruzada**: Se detectaron registros donde la ciudad no pertenecía al país etiquetado (ej. *San José* clasificado en *El Salvador*). La solución aplica un mapeo geográfico unívoco donde la ciudad actúa como fuente de verdad absoluta para corregir el país.
*   **Valores Numéricos Absurdos/Imposibles**: Se eliminaron ingresos negativos (ej. `-100,000.0` pesos/dólares) y outliers extremos no lógicos que alteraban las medias. Fueron re-imputados robustamente usando la **mediana** del dataset.
*   **Inconsistencias Transaccionales**: Se corrigieron registros que reportaban transacciones recientes de compra (`compras_ultimos_6m > 0`) pero un monto acumulado de `$0`. Se aplicó una imputación lógica secundaria basada en la mediana financiera.
*   **Ruido en la Ingesta (Encoding & Nulos)**: Se eliminaron caracteres corruptos e invisibles como marcas BOM (`\xef\xbb\xbf`) y caracteres especiales rotos debido a una codificación incorrecta de origen, forzando la lectura en Latin-1 y exportando en UTF-8 puro. Además, se impidió que los nulos se representaran como la cadena literal de texto `"nan"`.
*   **Estandarización de Estados**: Homogeneización de la columna `estado_cliente` (unificando variaciones de mayúsculas/minúsculas como `ACTIVO`, `activo`, `Inactivo` a categorías normalizadas).

### 2. Rigor Estadístico de Asociación
Para el análisis de correlación entre variables de alta asimetría (como ingresos y montos de compra):
*   El coeficiente tradicional de **Pearson** arrojaba falsos diagnósticos debido a su sensibilidad a valores extremos (outliers).
*   Se incorporó la **Correlación de Rangos de Spearman**, un estadístico no paramétrico y robusto ante asimetrías y distribuciones de cola larga, permitiendo medir relaciones monótonas de manera fiable.

### 3. Visualización y UX Premium de Resultados (Dashboard)
Sustituye reportes estáticos y planos por un **Dashboard Interactivo de Alta Gama** (`index.html`):
*   **Cálculo en Tiempo Real**: Toda la estadística descriptiva y las matrices de correlación (tanto Pearson como Spearman) se recalculan dinámicamente en el cliente al aplicar filtros geográficos o por segmento.
*   **Diseño de Vanguardia**: Estética oscura con glassmorphism, micro-animaciones CSS y gráficos interactivos de Plotly.js estructurados en pestañas funcionales (Resumen, Distribuciones, Rigor Estadístico, Auditoría de Calidad y Visualizador de Datos).

---

## Estructura del Proyecto

El proyecto está diseñado bajo un paradigma modular de programación orientada a objetos (POO):

*   [eda_package]: Paquete de procesamiento y análisis.
    *   [base.py]: Clase abstracta base del procesador.
    *   [loader.py]: Módulo de carga de archivos CSV con encoding sanitizado.
    *   [cleaner.py]: Motor de reglas de calidad e imputación de nulos.
    *   [statistics.py]: Motor de cálculo de descriptivos y correlación (Pearson y Spearman).
    *   [visualizer.py]: Módulo para generación de diagramas y heatmaps interactivos.
*   [notebook_unificado.ipynb]: Cuaderno de trabajo interactivo que documenta el análisis estadístico paso a paso.
*   [index.html]: Dashboard web interactivo para consumo y presentación gerencial.
*   [data/processed/clientes_clean.csv]: Dataset resultante depurado.
*   [reporte.md]: Informe ejecutivo respondiendo a las preguntas de negocio.

---

## Cómo Ejecutar el Proyecto

### Requisitos Previos
Asegúrate de contar con Python 3.8+ y las siguientes librerías instaladas:
```bash
pip install pandas numpy scipy seaborn matplotlib plotly
```

### Ejecutar el Pipeline de Limpieza
Para regenerar el conjunto de datos limpio a partir del archivo crudo, puedes ejecutar:
```bash
python -c "
from eda_package.loader import DataLoader
from eda_package.cleaner import DataCleaner
df_raw = DataLoader('clientes_dirty_semana2.csv').load_data()
df_clean = DataCleaner(df_raw).execute_pipeline()
df_clean.to_csv('data/processed/clientes_clean.csv', index=False, encoding='utf-8')
"
```

### Abrir el Dashboard
Simplemente abre el archivo [index.html] en cualquier navegador web moderno. No requiere servidor local (funciona de forma autónoma).
