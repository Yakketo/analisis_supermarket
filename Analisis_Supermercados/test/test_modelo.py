import sys
import unittest
import pandas as pd
import os
from src.analisis import DataAnalisis
from src.ModeloPredictivo import ModeloPredictivo 

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

class TestModeloPredictivo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '..', 'data')
        file_names = ['data_supermarket_1.csv', 'data_supermarket_2.csv', 'data_supermarket_3.csv']
        paths = [os.path.join(data_dir, file) for file in file_names]

        analisis = DataAnalisis(paths)
        analisis.load_and_clean_data()
        cls.data = analisis.get_cleaned_data()

    def test_prepare_features(self):
        model = ModeloPredictivo(self.data)
        X, y = model.prepare_features()

        # Verificamos que X no sea vacio y que tenga las columnas correctas
        self.assertFalse(X.empty)
        self.assertTrue('price' in X.columns)
        self.assertTrue('month' in X.columns)
        self.assertTrue('year' in X.columns)
        self.assertTrue('dayofweek' in X.columns)
        self.assertTrue('dayofyear' in X.columns)
        self.assertTrue('quarter' in X.columns)
        self.assertTrue('promotion_active' in X.columns)
        self.assertTrue('product_name' in X.columns)
        self.assertTrue('category' in X.columns)
        self.assertTrue('store_id' in X.columns)
        self.assertTrue('store_location' in X.columns)
        self.assertTrue('holiday' in X.columns)
        self.assertTrue('local_event' in X.columns)
        self.assertTrue('units_sold_lag_1' in X.columns)
        self.assertTrue('units_sold_lag_7' in X.columns)
        self.assertTrue('units_sold_diff_1' in X.columns) 
        self.assertTrue('units_sold_diff_7' in X.columns)
        self.assertFalse(y.empty)

    def test_train_model(self):
        model = ModeloPredictivo(self.data)

        # Probamos que el modelo se pueda entrenar
        model.train_model()
        # Verificamos que el modelo no sea None
        self.assertIsNotNone(model.model)
        self.assertIsNotNone(model.preprocessor)

    def test_predict(self):
        model = ModeloPredictivo(self.data)
        model.train_model()

        # Realizamos predicciones
        X, _ = model.prepare_features()
        y_pred = model.predict(X)

        # Verificamos que las predicciones no sean vacías
        self.assertFalse(y_pred.size == 0)

    def test_save_predictions(self):
        model = ModeloPredictivo(self.data)
        model.train_model()
        X, _ = model.prepare_features()
        y_pred = model.predict(X)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, '..', 'output', 'predicciones_test.csv') 

        model.save_predictions(self.data[['date']], y_pred, output_path)

        # Verificamos que el archivo de predicciones se haya guardado
        self.assertTrue(os.path.exists(output_path))
        os.remove(output_path) 

    def test_save_load_model(self):
        model = ModeloPredictivo(self.data)
        model.train_model()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, '..', 'models', 'modelo_test.pkl')

        model.save_model(model_path)
        self.assertTrue(os.path.exists(model_path))

        loaded_model = ModeloPredictivo(pd.DataFrame()) 
        loaded_model.load_model(model_path)

        self.assertIsNotNone(loaded_model.model)
        self.assertIsNotNone(loaded_model.preprocessor)

        os.remove(model_path) 

if __name__ == '__main__':
    unittest.main()