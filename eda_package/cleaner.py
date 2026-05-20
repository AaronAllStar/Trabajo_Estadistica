from .base import BaseDataProcessor
import pandas as pd
import numpy as np

class DataCleaner(BaseDataProcessor):
    """Subclase de BaseDataProcessor para limpieza de datos avanzada y de alta precisión."""
    def __init__(self, df: pd.DataFrame):
        super().__init__(df)

    def clean_column_names(self):
        # Eliminar el BOM del principio si existe (leído en latin1 como \xef\xbb\xbf o ï»¿)
        self.df.columns = (
            self.df.columns
            .str.replace(chr(239) + chr(187) + chr(191), '', regex=False)
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
        )
        return self

    def remove_duplicates(self):
        initial_shape = self.df.shape[0]
        self.df = self.df.drop_duplicates()
        print(f"[Limpieza] Removidas {initial_shape - self.df.shape[0]} filas duplicadas.")
        return self

    def clean_specific_columns(self):
        # 1. Edad: Limitar a rango lógico y coerción
        if 'edad' in self.df.columns:
            self.df['edad'] = pd.to_numeric(self.df['edad'], errors='coerce')
            self.df.loc[(self.df['edad'] < 15) | (self.df['edad'] > 100), 'edad'] = np.nan
        
        # 2. Ingresos mensuales: Limpieza de símbolos, strings inválidos, corrección de negativos y control de outliers
        if 'ingresos_mensuales' in self.df.columns:
            self.df['ingresos_mensuales'] = (
                self.df['ingresos_mensuales']
                .astype(str)
                .str.replace(r'[₡,]', '', regex=True)
                .str.replace(r'(?i)nd|sin dato|error|nan', 'nan', regex=True)
            )
            self.df['ingresos_mensuales'] = pd.to_numeric(self.df['ingresos_mensuales'], errors='coerce')
            # Corrección de ingresos negativos
            self.df.loc[self.df['ingresos_mensuales'] < 0, 'ingresos_mensuales'] = np.nan
            # Valores irreales como 25,000,000 en ingresos
            self.df.loc[self.df['ingresos_mensuales'] > 3000000, 'ingresos_mensuales'] = np.nan

        # 3. Monto total de compras: Limpieza de símbolos, corregir negativos, inconsistencias de compras e imputar errores
        if 'monto_total_compras' in self.df.columns:
            self.df['monto_total_compras'] = (
                self.df['monto_total_compras']
                .astype(str)
                .str.replace(r'[₡,]', '', regex=True)
                .str.replace(r'(?i)error|nan', 'nan', regex=True)
            )
            self.df['monto_total_compras'] = pd.to_numeric(self.df['monto_total_compras'], errors='coerce')
            # Corregir compras negativas
            self.df.loc[self.df['monto_total_compras'] < 0, 'monto_total_compras'] = np.nan
            # Outliers absurdos de compras
            self.df.loc[self.df['monto_total_compras'] > 2000000, 'monto_total_compras'] = np.nan
            
            # Regla de consistencia de compras: compras_ultimos_6m > 0 pero monto_total_compras == 0
            if 'compras_ultimos_6m' in self.df.columns:
                self.df['compras_ultimos_6m'] = pd.to_numeric(self.df['compras_ultimos_6m'], errors='coerce')
                self.df.loc[(self.df['compras_ultimos_6m'] > 0) & (self.df['monto_total_compras'] == 0), 'monto_total_compras'] = np.nan

        # 4. Score de riesgo: rango estándar de 0 a 1000
        if 'score_riesgo' in self.df.columns:
            self.df['score_riesgo'] = pd.to_numeric(self.df['score_riesgo'], errors='coerce')
            self.df.loc[(self.df['score_riesgo'] < 0) | (self.df['score_riesgo'] > 1000), 'score_riesgo'] = np.nan

        # 5. Tiempo de entrega (días): no puede ser negativo y valores absurdos > 60 se tratan como nulos
        if 'tiempo_entrega_dias' in self.df.columns:
            self.df['tiempo_entrega_dias'] = pd.to_numeric(self.df['tiempo_entrega_dias'], errors='coerce')
            self.df.loc[(self.df['tiempo_entrega_dias'] < 0) | (self.df['tiempo_entrega_dias'] > 60), 'tiempo_entrega_dias'] = np.nan

        # 6. Reclamos y compras_ultimos_6m: lógicos y no negativos
        if 'reclamos_ultimos_6m' in self.df.columns:
            self.df['reclamos_ultimos_6m'] = pd.to_numeric(self.df['reclamos_ultimos_6m'], errors='coerce')
            self.df.loc[(self.df['reclamos_ultimos_6m'] < 0) | (self.df['reclamos_ultimos_6m'] > 20), 'reclamos_ultimos_6m'] = np.nan

        if 'compras_ultimos_6m' in self.df.columns:
            # compras_ultimos_6m ya fue convertido en el paso 3, pero nos aseguramos del rango no negativo
            self.df.loc[(self.df['compras_ultimos_6m'] < 0) | (self.df['compras_ultimos_6m'] > 100), 'compras_ultimos_6m'] = np.nan

        # 7. Género: Estandarización estricta
        if 'genero' in self.df.columns:
            self.df['genero'] = self.df['genero'].astype(str).str.lower().str.strip()
            mapping = {
                'm': 'Masculino', 'masc': 'Masculino', 'male': 'Masculino', 'masculino': 'Masculino',
                'f': 'Femenino', 'fem': 'Femenino', 'female': 'Femenino', 'femenino': 'Femenino',
                'no indica': 'Desconocido', 'desconocido': 'Desconocido'
            }
            self.df['genero'] = self.df['genero'].map(mapping).fillna('Desconocido')

        # 8. País y Ciudad: Estandarización y Validación Geográfica
        if 'ciudad' in self.df.columns:
            self.df['ciudad'] = self.df['ciudad'].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()
            ciudad_map = {
                'San José': 'San José', 'San Jose': 'San José',
                'Puntarenas': 'Puntarenas', 'Alajuela': 'Alajuela', 'Cartago': 'Cartago',
                'Liberia': 'Liberia', 'Heredia': 'Heredia', 'Managua': 'Managua',
                'Ciudad de Guatemala': 'Ciudad de Guatemala', 'Antigua': 'Antigua',
                'San Salvador': 'San Salvador', 'Ciudad de Panamá': 'Ciudad de Panamá',
                'Ciudad de panama': 'Ciudad de Panamá', 'nan': 'Desconocido', 'Desconocido': 'Desconocido'
            }
            self.df['ciudad'] = self.df['ciudad'].map(ciudad_map).fillna('Desconocido')

        if 'pais' in self.df.columns:
            self.df['pais'] = self.df['pais'].astype(str).str.replace(r'\s+', ' ', regex=True).str.strip()
            pais_map = {
                'cost rica': 'Costa Rica', 'costa rica': 'Costa Rica', 'costarica': 'Costa Rica', 'cr': 'Costa Rica',
                'el salvador': 'El Salvador', 'salvador': 'El Salvador', 'esa': 'El Salvador',
                'nicaragua': 'Nicaragua', 'nicargua': 'Nicaragua', 'ni': 'Nicaragua',
                'guatemala': 'Guatemala', 'guate': 'Guatemala', 'gt': 'Guatemala',
                'panama': 'Panamá', 'panamá': 'Panamá', 'pan': 'Panamá',
                'nan': 'Desconocido', 'Desconocido': 'Desconocido'
            }
            self.df['pais'] = self.df['pais'].map(pais_map).fillna('Desconocido')

        # Regla de consistencia geográfica: la ciudad manda sobre el país
        if 'ciudad' in self.df.columns and 'pais' in self.df.columns:
            ciudad_to_pais = {
                'San José': 'Costa Rica',
                'Puntarenas': 'Costa Rica',
                'Alajuela': 'Costa Rica',
                'Cartago': 'Costa Rica',
                'Liberia': 'Costa Rica',
                'Heredia': 'Costa Rica',
                'Managua': 'Nicaragua',
                'Ciudad de Guatemala': 'Guatemala',
                'Antigua': 'Guatemala',
                'San Salvador': 'El Salvador',
                'Ciudad de Panamá': 'Panamá'
            }
            for city, country in ciudad_to_pais.items():
                self.df.loc[self.df['ciudad'] == city, 'pais'] = country

        # 9. Segmento: Estandarización
        if 'segmento' in self.df.columns:
            self.df['segmento'] = self.df['segmento'].astype(str).str.strip().str.capitalize()
            self.df['segmento'] = self.df['segmento'].replace({'Sin segmento': 'Desconocido', 'Nan': 'Desconocido'})

        # 10. Nivel de Satisfacción: Mapeo de ratings numéricos (1-5) a categóricos
        if 'nivel_satisfaccion' in self.df.columns:
            self.df['nivel_satisfaccion'] = self.df['nivel_satisfaccion'].astype(str).str.strip().str.capitalize()
            sat_map = {
                '1': 'Muy bajo', '2': 'Bajo', '3': 'Medio', '4': 'Alto', '5': 'Muy alto',
                'Muy bajo': 'Muy bajo', 'Bajo': 'Bajo', 'Medio': 'Medio', 'Alto': 'Alto', 'Muy alto': 'Muy alto',
                'Desconocido': 'Desconocido', 'Nan': 'Desconocido'
            }
            self.df['nivel_satisfaccion'] = self.df['nivel_satisfaccion'].map(sat_map).fillna('Desconocido')

        # 11. Canal preferido: Estandarización
        if 'canal_preferido' in self.df.columns:
            self.df['canal_preferido'] = self.df['canal_preferido'].astype(str).str.strip().str.capitalize()
            self.df['canal_preferido'] = self.df['canal_preferido'].replace({'Correo': 'Email', 'Whatsapp': 'WhatsApp', 'Sms': 'SMS', 'Nan': 'Desconocido'})

        # 12. Email y Teléfono inválidos
        if 'email' in self.df.columns:
            self.df['email'] = self.df['email'].astype(str).str.strip()
            self.df.loc[self.df['email'].str.contains(r'@@|sin correo|Desconocido|nan|none', case=False, na=True), 'email'] = 'Desconocido'

        if 'telefono' in self.df.columns:
            self.df['telefono'] = self.df['telefono'].astype(str).str.strip()
            self.df.loc[self.df['telefono'].str.contains(r'sin|123|Desconocido|nan|none', case=False, na=True), 'telefono'] = 'Desconocido'
            self.df.loc[self.df['telefono'].str.len() < 7, 'telefono'] = 'Desconocido'

        # 13. Estatus del Cliente: Estandarización
        if 'estado_cliente' in self.df.columns:
            self.df['estado_cliente'] = self.df['estado_cliente'].astype(str).str.strip().str.capitalize()
            estado_map = {
                'Activo': 'Activo', 'Inactivo': 'Inactivo', 'Bloqueado': 'Bloqueado', 'Pendiente': 'Pendiente',
                'Desconocido': 'Desconocido', 'Nan': 'Desconocido', 'None': 'Desconocido'
            }
            self.df['estado_cliente'] = self.df['estado_cliente'].map(estado_map).fillna('Desconocido')

        return self

    def fix_data_types(self):
        if 'fecha_registro' in self.df.columns:
            self.df['fecha_registro'] = self.df['fecha_registro'].astype(str).replace('sin fecha', np.nan)
            self.df['fecha_registro'] = pd.to_datetime(self.df['fecha_registro'], errors='coerce', format='mixed', dayfirst=True)
        return self
        
    def handle_missing_values(self):
        # Imputación inteligente: Variables numéricas con mediana
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            median_val = self.df[col].median()
            # Si toda la columna es nula, usar 0
            if pd.isna(median_val):
                median_val = 0
            self.df[col] = self.df[col].fillna(median_val)
            
        # Imputación de fechas
        if 'fecha_registro' in self.df.columns:
            if self.df['fecha_registro'].isnull().any():
                mode_date = self.df['fecha_registro'].mode()
                fill_date = mode_date[0] if not mode_date.empty else pd.Timestamp('2025-01-01')
                self.df['fecha_registro'] = self.df['fecha_registro'].fillna(fill_date)
            
        # Categóricas con Desconocido
        categorical_cols = self.df.select_dtypes(exclude=[np.number, 'datetime64[ns]']).columns
        for col in categorical_cols:
            self.df[col] = self.df[col].fillna('Desconocido')
            # Evitar filtración de strings 'nan' / 'None'
            self.df[col] = self.df[col].astype(str).replace({
                'nan': 'Desconocido', 'None': 'Desconocido', 'NaN': 'Desconocido', '': 'Desconocido'
            })
            
        # Re-verificar consistencia cruzada de compras después de imputaciones
        if 'compras_ultimos_6m' in self.df.columns and 'monto_total_compras' in self.df.columns:
            self.df.loc[(self.df['compras_ultimos_6m'] > 0) & (self.df['monto_total_compras'] == 0), 'monto_total_compras'] = np.nan
            # Re-imputar monto_total_compras si fue anulado por la inconsistencia
            if self.df['monto_total_compras'].isnull().any():
                median_monto = self.df['monto_total_compras'].median()
                self.df['monto_total_compras'] = self.df['monto_total_compras'].fillna(median_monto if not pd.isna(median_monto) else 0)
            
        return self

    def execute_pipeline(self) -> pd.DataFrame:
        """Ejecuta el pipeline de limpieza completo y retorna el DataFrame limpio."""
        self.clean_column_names()
        self.remove_duplicates()
        self.clean_specific_columns()
        self.fix_data_types()
        self.handle_missing_values()
        print("[Limpieza] Pipeline de limpieza finalizado con alta precisión.")
        return self.df
