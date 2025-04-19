import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
from src.analisis import DataAnalisis
from src.ModeloPredictivo import ModeloPredictivo  

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

# Cargamos los datos y entrenamos el modelo
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')

file_names = ['data_supermarket_1.csv', 'data_supermarket_2.csv', 'data_supermarket_3.csv']
paths = [os.path.join(data_dir, file) for file in file_names]

analisis = DataAnalisis(paths)
analisis.load_and_clean_data()
full_data = analisis.get_cleaned_data()

# Creamos el modelo predictivo
model_predictor = ModeloPredictivo(full_data.copy()) 

# Entrenamos el modelo 
model_predictor.train_model()

# Preparamos las características y realizamos las predicciones
X_untransformed, _ = model_predictor.prepare_features() 

# Realizamos las predicciones
y_pred = model_predictor.predict(X_untransformed)

# Alineamos las fechas con las predicciones usando el índice del DataFrame interno
dates_pred = model_predictor.data.loc[X_untransformed.index, 'date']
real_values = model_predictor.data.loc[X_untransformed.index, 'units_sold']

# Aseguramos que las predicciones tengan la misma longitud que las fechas alineadas
if len(y_pred) != len(dates_pred):
    print("Advertencia: La longitud de las predicciones no coincide con la longitud de las fechas alineadas.")

# Graficamos las predicciones y los valores reales
plt.figure(figsize=(12, 6)) 
plt.plot(dates_pred, real_values, label='Real', color='blue', alpha=0.7)
plt.plot(dates_pred, y_pred, label='Predicción', color='red', linestyle='--', alpha=0.7)
plt.xlabel('Fecha')
plt.ylabel('Cantidad de Unidades Vendidas')
plt.title('Predicciones de Ventas vs Ventas Reales')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True) 
plt.tight_layout()
plt.show()

# Gráfico de dispersión de predicciones vs reales
plt.figure(figsize=(8, 8))
plt.scatter(real_values, y_pred, color='purple', alpha=0.5)
plt.xlabel('Ventas Reales')
plt.ylabel('Ventas Predichas')
plt.title('Dispersión de Predicciones vs Ventas Reales')
plt.plot([real_values.min(), real_values.max()], [real_values.min(), real_values.max()], color='black', linestyle='--', linewidth=1) 
plt.grid(True)
plt.tight_layout()
plt.show()

# Gráfico de residuos
residuals = y_pred - real_values
plt.figure(figsize=(12, 6))
plt.plot(dates_pred, residuals, label='Residuos', color='orange', alpha=0.7)
plt.axhline(y=0, color='black', linestyle='--', linewidth=1) 
plt.xlabel('Fecha')
plt.ylabel('Residuos (Predicción - Real)')
plt.title('Residuos del Modelo a lo Largo del Tiempo')
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()