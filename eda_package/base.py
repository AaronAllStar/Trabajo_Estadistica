import pandas as pd

class BaseDataProcessor:
    """Clase base para el procesamiento de datos. Implementa POO y Herencia."""
    def __init__(self, df: pd.DataFrame):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Los datos deben ser un DataFrame de Pandas.")
        self.df = df.copy()

    def get_data(self) -> pd.DataFrame:
        """Retorna el DataFrame actual."""
        return self.df

    def update_data(self, new_df: pd.DataFrame):
        """Actualiza el DataFrame interno."""
        self.df = new_df.copy()
