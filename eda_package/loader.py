import pandas as pd

class DataLoader:
    """Clase para cargar datasets."""
    def __init__(self, filepath):
        self.filepath = filepath

    def load_data(self):
        try:
            df = pd.read_csv(self.filepath)
            print(f"Dataset cargado exitosamente. Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
            return df
        except Exception as e:
            print(f"Error al cargar el dataset: {e}")
            return None
