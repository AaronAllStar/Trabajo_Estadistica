# Reporte Ejecutivo de Resultados

A continuación se responde de manera directa y concisa a las preguntas clave del análisis tras la depuración y estructuración de los datos.

### 1. ¿Cómo se distribuyen demográficamente los clientes (edad, género, país)?
* **Edad:** La distribución de edad tiene una **media de 34 años** y es asimétrica hacia la derecha (cola hacia los más adultos).
* **Género:** La distribución de género muestra un balance casi equitativo entre clientes masculinos y femeninos, con una proporción mínima que prefiere no indicarlo.
* **País:** El volumen principal de clientes está altamente concentrado en **Nicaragua, El Salvador y Guatemala**, mientras que Costa Rica y Panamá representan una fracción menor del mercado.

### 2. ¿Qué tan asimétricos son los ingresos mensuales y los hábitos de compra?
* **Alta asimetría positiva:** Ambas variables presentan una asimetría muy fuerte hacia la derecha.
* Esto significa que la gran mayoría de los clientes tiene ingresos y compras bajas/medias, mientras que un **grupo muy reducido (outliers y clientes Premium/Oro)** concentra niveles de gasto e ingresos desproporcionadamente altos. Por ello, la media es engañosa y la **mediana** es la mejor representación del cliente típico.

### 3. ¿Existe una correlación lineal real entre ingresos, compras y score de riesgo?
* **Ingresos vs. Compras:** Sí, existe una **correlación lineal positiva moderada**. Los clientes con mayores ingresos mensuales tienden a gastar más montos totales, aunque la varianza aumenta en los estratos más altos.
* **Score de Riesgo:** **No.** El score de riesgo no tiene ninguna correlación estadística ($r \approx 0$) ni con los ingresos ni con el monto de compras. Se comporta como una variable completamente independiente.
