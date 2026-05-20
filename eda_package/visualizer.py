from .base import BaseDataProcessor
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

class Visualizer(BaseDataProcessor):
    """Subclase de BaseDataProcessor para visualización de datos usando librerías estáticas e interactivas."""
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        sns.set_theme(style="whitegrid")

    def plot_histogram(self, column: str, bins: int = 30, interactive: bool = True):
        """Crea un histograma de una columna numérica."""
        if interactive:
            fig = px.histogram(self.df, x=column, nbins=bins, title=f'Distribución de {column}', 
                               template="plotly_dark", color_discrete_sequence=['#38bdf8'])
            return fig
        else:
            plt.figure(figsize=(10, 6))
            sns.histplot(self.df[column], kde=True, bins=bins, color='teal')
            plt.title(f'Distribución de {column}')
            plt.show()

    def plot_correlation_matrix(self, interactive: bool = True, method: str = 'pearson'):
        """Grafica la matriz de correlación (pearson, spearman, kendall)."""
        numeric_df = self.df.select_dtypes(include=['float64', 'int64'])
        corr = numeric_df.corr(method=method)
        method_title = 'Pearson' if method == 'pearson' else 'Spearman'
        if interactive:
            fig = px.imshow(corr, text_auto=True, title=f'Matriz de Correlación ({method_title})', 
                            template="plotly_dark", color_continuous_scale='Viridis')
            return fig
        else:
            plt.figure(figsize=(12, 8))
            sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
            plt.title(f'Matriz de Correlación ({method_title})')
            plt.show()

    def plot_boxplots(self, columns=None, interactive: bool = True):
        """Crea boxplots para detectar outliers visualmente."""
        if columns is None:
            columns = self.df.select_dtypes(include=['float64', 'int64']).columns
            
        if interactive:
            fig = go.Figure()
            for col in columns:
                fig.add_trace(go.Box(y=self.df[col], name=col))
            fig.update_layout(title="Detección de Outliers (Boxplots)", template="plotly_dark")
            return fig
        else:
            plt.figure(figsize=(15, 8))
            sns.boxplot(data=self.df[columns], palette="Set2")
            plt.xticks(rotation=45)
            plt.title("Detección de Outliers (Boxplots)")
            plt.show()
            
    def plot_categorical_count(self, column: str, interactive: bool = True):
        """Grafica el conteo de categorías."""
        counts = self.df[column].value_counts().reset_index()
        counts.columns = [column, 'count']
        if interactive:
            fig = px.bar(counts, x=column, y='count', title=f'Conteo de {column}',
                         template="plotly_dark", color='count', color_continuous_scale='Bluered')
            return fig
        else:
            plt.figure(figsize=(10, 6))
            sns.barplot(data=counts, x=column, y='count', palette='viridis')
            plt.title(f'Conteo de {column}')
            plt.xticks(rotation=45)
            plt.show()
