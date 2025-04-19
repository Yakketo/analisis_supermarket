import pandas as pd
import os

class DataAnalisis:
    def __init__(self, paths):
        self.paths = paths
        self.full_data = None

    # Funcion para cargar los datos y limpiarlos
    def load_and_clean_data(self):
        # Cargamos los archivos CSV y los juntamos
        data_frames = [pd.read_csv(path) for path in self.paths]
        self.full_data = pd.concat(data_frames, ignore_index=True)

        self.clean_data()

    # Funcion para limpiar los datos
    def clean_data(self):

        # Verificamos si hay columnas con valores null, y si las hay se eliminan 
        null_sums = self.full_data.isnull().sum()
        if null_sums.any():
            print("Valores nulos por columna antes de eliminar:")
            print(null_sums)
            cols_to_drop = [col for col in self.full_data.columns if self.full_data[col].isnull().any() and col not in ['holiday', 'local_event']]
            if cols_to_drop:
                self.full_data = self.full_data.drop(columns=cols_to_drop)
            if self.full_data['date'].isnull().any():
                self.full_data = self.full_data.dropna(subset=['date'])

        # Verificamos que la fecha tiene un valor válido
        self.full_data['date'] = pd.to_datetime(self.full_data['date'], errors='coerce')
        if self.full_data['date'].isnull().sum() > 0:
            self.full_data = self.full_data.dropna(subset=['date'])

        # Verificamos los tipos de datos y los convertimos si fuera necesario
        print(self.full_data.dtypes)

        self.full_data['price'] = self.full_data['price'].astype(float)
        self.full_data['units_sold'] = self.full_data['units_sold'].astype(int)
        self.full_data['stock_after'] = self.full_data['stock_after'].astype(int)
        self.full_data['promotion_active'] = self.full_data['promotion_active'].astype('Int64') 
       

        # Verificamos si hay filas con valores duplicados
        if self.full_data.duplicated().sum() > 0:
            self.full_data = self.full_data.drop_duplicates()

        print("Tipos de datos después de la conversión:")
        print(self.full_data.dtypes)

        self.remove_outliers()

        # Verificación lógica 
        self.full_data = self.full_data[
            (self.full_data['price'] >= 0) &
            (self.full_data['units_sold'] >= 0) &
            (self.full_data['stock_after'] >= 0) &
            (self.full_data['promotion_active'].isin([0, 1, pd.NA])) 
        ]

    # Funcion para eliminar los outliers
    def remove_outliers(self):
        Q1 = self.full_data['price'].quantile(0.25)
        Q3 = self.full_data['price'].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR

        outliers = self.full_data[(self.full_data['price'] < limite_inferior) | (self.full_data['price'] > limite_superior)]
        print(f"Se han encontrado {outliers.shape[0]} valores atípicos en price y se eliminaron")
        self.full_data = self.full_data[~((self.full_data['price'] < limite_inferior) | (self.full_data['price'] > limite_superior))]

    # Funcion para devolver los datos despues de la limpieza
    def get_cleaned_data(self):
        return self.full_data