from analisis import DataAnalisis
from  ModeloPredictivo import ModeloPredictivo  
import os
import pandas as pd


script_dir = os.path.dirname(os.path.abspath(__file__))
# Construimos la ruta a la carpeta data relativa al directorio del script
data_dir = os.path.join(script_dir, '..', 'data')
file_names = ['data_supermarket_1.csv', 'data_supermarket_2.csv', 'data_supermarket_3.csv']
paths = [os.path.join(data_dir, file) for file in file_names]

# Imprimimos el contenido de la lista paths
print("Rutas que se pasarán a DataAnalisis:", paths)

# Definimos la ruta donde se guardara o se cargara el modelo entrenado
model_dir = os.path.join(script_dir, '..', 'models')
os.makedirs(model_dir, exist_ok=True)
model_path = os.path.join(model_dir, 'modelo_entrenado.pkl')

# Creamos un objeto de la clase analisis
analisis = DataAnalisis(paths)

# Cargamos y limpiamos los datos
analisis.load_and_clean_data()

# Obtenemos los datos limpios
full_data = analisis.get_cleaned_data()

# Guardamos los datos limpios en un archivo CSV
output_dir = os.path.join(script_dir, '..', 'output')
os.makedirs(output_dir, exist_ok=True)
cleaned_data_path = os.path.join(output_dir, 'datos_limpios.csv')
full_data.to_csv(cleaned_data_path, index=False)
print(f"Datos limpios guardados en: {cleaned_data_path}")

# Creamos el modelo predictivo pasandole una copia para no afectar al original
model_predictor = ModeloPredictivo(full_data.copy()) 

# Verificamos si ya existe el modelo guardado
if os.path.exists(model_path):
    model_predictor.load_model(model_path)
    print(f"Modelo cargado desde: {model_path}")
else:
    model_predictor.train_model()
    model_predictor.save_model(model_path)
    print(f"Modelo entrenado y guardado en: {model_path}")

# Preparamos los datos de entrada para predecir
X_predict, _ = model_predictor.prepare_features()

# Realizamos predicciones
y_pred = model_predictor.predict(X_predict)

# Creamos el DataFrame de predicciones utilizando el índice de X_predict
predictions_df = pd.DataFrame({'date': model_predictor.data.loc[X_predict.index, 'date'],
                                 'predicted_units_sold': y_pred.round(0).astype(int)})

# Añadimos las ventas reales si están disponibles, usando el mismo indice
if 'units_sold' in model_predictor.data.columns:
    predictions_df['real_units_sold'] = model_predictor.data.loc[X_predict.index, 'units_sold']

# Definimos la ruta donde se guardaran las predicciones
output_dir = os.path.join(script_dir, '..', 'output')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'predicciones.csv')

# Guardamos las predicciones en un archivo CSV en la carpeta output
predictions_df.to_csv(output_path, index=False)

print(f"Predicciones guardadas en: {output_path}")