from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

class ModeloPredictivo:
    # Inicializamos la clase ModeloPredictivo con los datos
    def __init__(self, data):
        self.data = data.copy()
        self.model = None
        self.preprocessor = None

    # Preparamos las caracteristicas del modelo, incluyendo la creación de variables de retardo y temporales
    def prepare_features(self):
        self.data['date'] = pd.to_datetime(self.data['date'])
        self.data = self.data.sort_values(by='date')
        self.data['units_sold_lag_1'] = self.data['units_sold'].shift(1)
        self.data['units_sold_lag_7'] = self.data['units_sold'].shift(7)
        self.data['units_sold_diff_1'] = self.data['units_sold'].diff(1)
        self.data['units_sold_diff_7'] = self.data['units_sold'].diff(7)
        self.data['month'] = self.data['date'].dt.month
        self.data['year'] = self.data['date'].dt.year
        self.data['dayofweek'] = self.data['date'].dt.dayofweek
        self.data['dayofyear'] = self.data['date'].dt.dayofyear
        self.data['quarter'] = self.data['date'].dt.quarter
        self.data['promotion_active'] = self.data['promotion_active'].fillna(0).astype(int)
        categorical_features = ['product_name', 'category', 'store_id', 'store_location', 'holiday', 'local_event']
        numerical_features = ['price', 'month', 'year', 'dayofweek', 'dayofyear', 'quarter', 'promotion_active',
                                'units_sold_lag_1', 'units_sold_lag_7', 'units_sold_diff_1', 'units_sold_diff_7']
        self.data = self.data.dropna()
        X = self.data[categorical_features + numerical_features]
        y = self.data['units_sold']
        return X, y

    # Creamos un pipeline de preprocesamiento para características numericas y categoricas
    def create_preprocessing_pipeline(self, categorical_features, numerical_features):
        numerical_transformer = StandardScaler()
        categorical_transformer = OneHotEncoder(handle_unknown='ignore')
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, numerical_features),
                ('cat', categorical_transformer, categorical_features)])
        return preprocessor

    # Entrenamos el modelo predictivo utilizando RandomForestRegressor
    def train_model(self, test_size=0.2, random_state=42):
        X, y = self.prepare_features()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        categorical_features = ['product_name', 'category', 'store_id', 'store_location', 'holiday', 'local_event']
        numerical_features = ['price', 'month', 'year', 'dayofweek', 'dayofyear', 'quarter', 'promotion_active',
                                'units_sold_lag_1', 'units_sold_lag_7', 'units_sold_diff_1', 'units_sold_diff_7']
        self.preprocessor = self.create_preprocessing_pipeline(categorical_features, numerical_features)
        self.model = Pipeline(steps=[('preprocessor', self.preprocessor),
                                       ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))])
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        print("Modelo Entrenado: Random Forest Regressor con Ingeniería de Características y Preprocesamiento")
        print("Error Cuadrático Medio (MSE):", mse)
        print("Coeficiente de Determinación (R²):", r2)
        print("Error Absoluto Medio (MAE):", mae)

    # Realizamos predicciones utilizando el modelo entrenado
    def predict(self, X):
        if self.model is None:
            raise Exception("El modelo no ha sido entrenado.")
        return self.model.predict(X)

    # Guardamos las predicciones en un archivo CSV
    def save_predictions(self, original_X, y_pred, output_path):
        predictions = pd.DataFrame({
            'date': original_X['date'],
            'real_units_sold': self.data.loc[original_X.index, 'units_sold'] if 'units_sold' in self.data.columns else np.nan,
            'predicted_units_sold': y_pred.round(0).astype(int)
        })
        predictions.to_csv(output_path, index=False)

    # Guardamos el modelo entrenado en un archivo
    def save_model(self, path):
        joblib.dump(self.model, path)

    # Carga un modelo previamente entrenado desde un archivo
    def load_model(self, path):
        self.model = joblib.load(path)