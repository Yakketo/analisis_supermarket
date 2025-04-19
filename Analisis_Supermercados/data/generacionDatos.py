import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from collections import defaultdict

# Ciudades españolas con datos climáticos aproximados
spanish_cities_climate = {
    'Madrid': {'summer_temp_avg': 28, 'rain_summer_prob': 0.1, 'winter_temp_avg': 7, 'rain_winter_prob': 0.3, 'event_prob_base': 0.03},
    'Barcelona': {'summer_temp_avg': 27, 'rain_summer_prob': 0.2, 'winter_temp_avg': 9, 'rain_winter_prob': 0.4, 'event_prob_base': 0.05},
    'Valencia': {'summer_temp_avg': 30, 'rain_summer_prob': 0.15, 'winter_temp_avg': 10, 'rain_winter_prob': 0.35, 'event_prob_base': 0.04},
    'Sevilla': {'summer_temp_avg': 35, 'rain_summer_prob': 0.05, 'winter_temp_avg': 12, 'rain_winter_prob': 0.25, 'event_prob_base': 0.06},
    'Bilbao': {'summer_temp_avg': 22, 'rain_summer_prob': 0.3, 'winter_temp_avg': 8, 'rain_winter_prob': 0.6, 'event_prob_base': 0.04},
    'Málaga': {'summer_temp_avg': 30, 'rain_summer_prob': 0.1, 'winter_temp_avg': 11, 'rain_winter_prob': 0.3, 'event_prob_base': 0.035},
    'Alicante': {'summer_temp_avg': 31, 'rain_summer_prob': 0.1, 'winter_temp_avg': 10, 'rain_winter_prob': 0.3, 'event_prob_base': 0.045},
    'Zaragoza': {'summer_temp_avg': 32, 'rain_summer_prob': 0.1, 'winter_temp_avg': 6, 'rain_winter_prob': 0.2, 'event_prob_base': 0.03},
    'Murcia': {'summer_temp_avg': 33, 'rain_summer_prob': 0.08, 'winter_temp_avg': 9, 'rain_winter_prob': 0.2, 'event_prob_base': 0.03},
    'Palma de Mallorca': {'summer_temp_avg': 29, 'rain_summer_prob': 0.2, 'winter_temp_avg': 10, 'rain_winter_prob': 0.4, 'event_prob_base': 0.05},
}

# Nombres de productos y categorías
products = ['Leche Entera', 'Pan de Molde', 'Manzanas Fuji', 'Detergente Líquido', 'Cerveza Lager', 'Yogur Natural', 'Pasta Italiana', 'Papel Higiénico', 'Pollo Fresco', 'Aceite de Oliva', 'Helado de Vainilla', 'Turrón de Almendras', 'Vino Tinto Rioja', 'Paraguas', 'Protector Solar']
categories = ['Lácteos', 'Panadería', 'Frutas y Verduras', 'Limpieza', 'Bebidas', 'Lácteos', 'Alimentación', 'Higiene', 'Carnes', 'Alimentación', 'Congelados', 'Alimentación (Navidad)', 'Bebidas', 'Hogar', 'Cuidado Personal']
product_category = dict(zip(products, categories))

# Rango de precios ajustados por categoría
category_price_range = {
    'Lácteos': (0.5, 3.5), 'Panadería': (0.5, 3.0), 'Frutas y Verduras': (0.8, 6.0), 'Limpieza': (1.2, 8.0),
    'Bebidas': (0.8, 12.0), 'Alimentación': (0.6, 10.0), 'Higiene': (0.9, 6.0), 'Carnes': (2.5, 15.0),
    'Congelados': (1.5, 9.0), 'Alimentación (Navidad)': (3.0, 25.0), 'Hogar': (5.0, 20.0), 'Cuidado Personal': (3.0, 15.0)
}

# Stock máximo por producto (simulado)
max_stock = {product: random.randint(50, 200) for product in products}

# IDs de tiendas
store_ids = [f'S{i:03d}' for i in range(1, 51)]

# Festivos nacionales en España (con fechas para 2024 y 2025)
national_holidays = {
    (1, 1): "Año Nuevo", (1, 6): "Reyes Magos", (5, 1): "Día del Trabajo", (8, 15): "Asunción de la Virgen",
    (10, 12): "Fiesta Nacional de España", (11, 1): "Todos los Santos", (12, 6): "Día de la Constitución Española",
    (12, 8): "Inmaculada Concepción", (12, 25): "Navidad",
    (2024, 3, 28): "Jueves Santo", (2024, 3, 29): "Viernes Santo",
    (2025, 4, 17): "Jueves Santo", (2025, 4, 18): "Viernes Santo",
}

# Festivos regionales
regional_holidays = {
    'Madrid': {(5, 2): "Día de la Comunidad de Madrid"},
    'Barcelona': {(9, 11): "Diada Nacional de Cataluña"},
    'Valencia': {(3, 19): "Las Fallas", (10, 9): "Día de la Comunidad Valenciana"},
    'Sevilla': {(4, 18): "Feria de Abril", (8, 15): "Virgen de los Reyes"},
    'Bilbao': {(7, 25): "Santiago Apóstol"},
    'Málaga': {(8, 19): "Toma de Málaga"},
    'Alicante': {(6, 24): "Hogueras de San Juan"},
    'Zaragoza': {(4, 23): "Día de Aragón"},
    'Murcia': {(6, 9): "Día de la Región de Murcia"},
    'Palma de Mallorca': {(3, 1): "Día de las Islas Baleares"},
}

# Simulación básica de ventas pasadas (para ajustar probabilidad de eventos)
past_sales_events = defaultdict(lambda: defaultdict(int)) # {(ciudad, tipo_evento): conteo}

def generate_realistic_data(num_rows, start_date, end_date):
    data = []
    for i in range(num_rows):
        product_name = random.choice(products)
        category = product_category[product_name]

        price_range = category_price_range[category]
        price = round(random.uniform(price_range[0], price_range[1]), 2)

        initial_stock = max_stock[product_name]
        stock_before = random.randint(0, initial_stock)
        units_sold_base = int(np.random.normal(loc=8, scale=4))
        if units_sold_base < 1: units_sold_base = 1

        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        weekday = date.weekday()
        year = date.year
        month = date.month
        day = date.day
        store_id = random.choice(store_ids)
        store_location = random.choice(list(spanish_cities_climate.keys()))
        climate = spanish_cities_climate[store_location]

        promotion_active = 0
        holiday = "Sin Festivo"
        local_event = "Sin Evento"

        # Promociones
        if date.weekday() >= 4 and random.random() < 0.6:
            promotion_active = 1
            promotion_type = random.choice(["Descuento%", "2x1", "Precio Fijo"])
            discount = random.uniform(0.15, 0.5) if promotion_type == "Descuento%" else 0
            if promotion_type == "Precio Fijo":
                price = round(price * random.uniform(0.6, 0.8), 2)
            else:
                price = round(price * (1 - discount), 2)
            units_sold_base = int(units_sold_base * (1 + discount * 3))

        # Festivos nacionales
        if (month, day) in national_holidays or (year, month, day) in national_holidays:
            holiday_name = national_holidays.get((month, day)) or national_holidays.get((year, month, day))
            holiday = holiday_name if holiday_name else "Sin Festivo"
            units_sold_base = int(units_sold_base * random.uniform(0.6, 1.5))

        # Festivos regionales
        if store_location in regional_holidays and (month, day) in regional_holidays[store_location]:
            holiday = regional_holidays[store_location][(month, day)]
            units_sold_base = int(units_sold_base * random.uniform(1.3, 1.8))

        # Variabilidad de eventos locales por temporada/ciudad (ajuste de probabilidad)
        event_probability = climate['event_prob_base']
        if month in [4, 5, 6] and store_location in ['Sevilla', 'Valencia']: # Ferias y festivales de primavera
            event_probability *= 1.5
        if month in [7, 8] and store_location in ['Málaga', 'Alicante', 'Palma de Mallorca']: # Eventos de verano
            event_probability *= 1.2
        if random.random() < event_probability:
            event_type = random.choice(["Feria Local", "Concierto Grande", "Evento Deportivo Importante", "Mercado Semanal", "Festival de Música"])
            local_event = event_type
            if (store_location, event_type) not in past_sales_events:
                past_sales_events[(store_location, event_type)] = 0
                past_sales_events[(store_location, event_type)] += 1 # Simulación de registro de eventos pasados
            impact = 1 + random.uniform(0.2, 0.8)
            units_sold_base = int(units_sold_base * impact)
            if "Deportivo" in event_type and category == 'Bebidas':
                units_sold_base = int(units_sold_base * 1.6)

        # Efectos del clima
        temp_effect = 1.0
        rain_effect = 1.0
        if month in [6, 7, 8]:
            temp_effect += (climate['summer_temp_avg'] - 25) * 0.01
            if random.random() < climate['rain_summer_prob']:
                rain_effect = 0.7
                if category == 'Paraguas': units_sold_base *= 6
                if product_name == 'Protector Solar': units_sold_base *= 0.4
        elif month in [11, 12, 1, 2]:
            if random.random() < climate['rain_winter_prob']:
                rain_effect = 0.8
                if category == 'Paraguas': units_sold_base *= 4

        units_sold_base = int(units_sold_base * temp_effect * rain_effect)

        # Estacionalidad detallada
        if month == 12:
            if product_name == 'Turrón de Almendras': units_sold_base = int(units_sold_base * 5)
            if product_name == 'Vino Tinto Rioja': units_sold_base = int(units_sold_base * 2)
        elif month == 7 and product_name == 'Cerveza Lager':
            units_sold_base = int(units_sold_base * 1.8)
        elif month in [1, 9]:
            if category == 'Panadería': units_sold_base = int(units_sold_base * 1.1)
            if category == 'Lácteos': units_sold_base = int(units_sold_base * 1.05)

        # Sensibilidad al precio
        price_normalized = (price - price_range[0]) / (price_range[1] - price_range[0] + 1e-6)
        units_sold = max(0, int(units_sold_base * (1 - price_normalized * 0.7)))

        # Variabilidad semanal
        if weekday < 5:
            units_sold = int(units_sold * random.uniform(0.7, 1.0))
        elif weekday == 5:
            units_sold = int(units_sold * random.uniform(1.2, 1.5))
        else:
            units_sold = int(units_sold * random.uniform(1.0, 1.3))

        # Límite de stock
        units_sold = min(units_sold, stock_before)
        stock_after = max(0, stock_before - units_sold)

        data.append([product_name, price, category, units_sold, stock_after, date.strftime('%Y-%m-%d'), store_id, store_location, promotion_active, holiday, local_event])

    return pd.DataFrame(data, columns=['product_name', 'price', 'category', 'units_sold', 'stock_after', 'date', 'store_id', 'store_location', 'promotion_active', 'holiday', 'local_event'])

# Generar los 3 archivos con realismo abismal (y optimizaciones futuras)
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
num_rows_per_file = 1000 # Puedes aumentar esto para probar optimizaciones

df1 = generate_realistic_data(num_rows_per_file, start_date, end_date)
df2 = generate_realistic_data(num_rows_per_file, start_date, end_date)
df3 = generate_realistic_data(num_rows_per_file, start_date, end_date)

df1.to_csv('data_supermarket_1.csv', index=False)
df2.to_csv('data_supermarket_2.csv', index=False)
df3.to_csv('data_supermarket_3.csv', index=False)

print("Se han generado los 3 archivos CSV con realismo abismal (y listos para optimización a gran escala).")
print("Ejemplo de conteo de eventos pasados (simulado):", past_sales_events)