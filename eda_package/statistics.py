from .base import BaseDataProcessor
import pandas as pd
import numpy as np
from scipy import stats

class StatisticalAnalysis(BaseDataProcessor):
    """Subclase de BaseDataProcessor para análisis estadístico."""
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)
        self.numeric_cols = self.df.select_dtypes(include=[np.number]).columns

    def get_basic_stats(self):
        """Calcula media, mediana, moda y desviación estándar."""
        stats_df = pd.DataFrame()
        stats_df['Media'] = self.df[self.numeric_cols].mean()
        stats_df['Mediana'] = self.df[self.numeric_cols].median()
        stats_df['Desv_Estandar'] = self.df[self.numeric_cols].std()
        
        modas = []
        for col in self.numeric_cols:
            mode_val = self.df[col].mode()
            modas.append(mode_val.iloc[0] if not mode_val.empty else np.nan)
        stats_df['Moda'] = modas
        
        return stats_df

    def get_percentiles(self, percentiles=[0.25, 0.5, 0.75, 0.90, 0.99]):
        """Calcula los percentiles."""
        return self.df[self.numeric_cols].quantile(percentiles).T

    def get_shape_stats(self):
        """Calcula skewness y kurtosis usando Pandas y SciPy."""
        shape_stats = pd.DataFrame()
        shape_stats['Skewness (Pandas)'] = self.df[self.numeric_cols].skew()
        shape_stats['Kurtosis (Pandas)'] = self.df[self.numeric_cols].kurtosis()
        return shape_stats

    def get_correlations(self, method='pearson'):
        """Calcula la matriz de correlación (pearson, spearman, kendall)."""
        return self.df[self.numeric_cols].corr(method=method)

    def detect_outliers_iqr(self, column: str):
        """Detección de outliers mediante rango intercuartílico (IQR)."""
        if column not in self.numeric_cols:
            raise ValueError(f"La columna {column} no es numérica.")
            
        Q1 = self.df[column].quantile(0.25)
        Q3 = self.df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = self.df[(self.df[column] < lower_bound) | (self.df[column] > upper_bound)]
        
        return {
            'column': column,
            'outliers_count': outliers.shape[0],
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'outliers_data': outliers
        }

    def run_full_analysis(self):
        """Ejecuta todos los análisis y los retorna en un diccionario."""
        return {
            "Estadísticas Básicas": self.get_basic_stats(),
            "Percentiles": self.get_percentiles(),
            "Forma de la Distribución": self.get_shape_stats(),
            "Correlaciones": self.get_correlations(method='pearson'),
            "Correlaciones Spearman": self.get_correlations(method='spearman')
        }
