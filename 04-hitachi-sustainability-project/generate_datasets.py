import pandas as pd
import numpy as np

np.random.seed(42)

# --- Dataset de Consumo Energético (simulado) ---
fechas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='H')

data_energia = {
    'Timestamp': fechas,
    'Consumo_kWh': np.random.uniform(50, 200, size=len(fechas)).round(2),
    'Temperatura_C': np.random.uniform(15, 35, size=len(fechas)).round(2),
    'Humedad_Porcentaje': np.random.uniform(40, 80, size=len(fechas)).round(2),
    'Produccion_MWh': np.random.uniform(10, 50, size=len(fechas)).round(2)
}
energia_df = pd.DataFrame(data_energia)
energia_df.to_csv('/home/ubuntu/data-analytics-portfolio/04-hitachi-sustainability-project/data/hitachi_energia_2023.csv', index=False)

# --- Dataset de Emisiones de CO2 (simulado) ---

data_co2 = {
    'Timestamp': pd.to_datetime(np.random.choice(fechas, size=5000)),
    'Emisiones_CO2_ton': np.random.uniform(0.1, 1.5, size=5000).round(2),
    'Fuente_Emision': np.random.choice(['Generacion_Electrica', 'Transporte', 'Procesos_Industriales'], size=5000)
}
emisiones_co2_df = pd.DataFrame(data_co2)
emisiones_co2_df.to_csv('/home/ubuntu/data-analytics-portfolio/04-hitachi-sustainability-project/data/hitachi_emisiones_co2_2023.csv', index=False)

print("Datasets simulados para Hitachi Vantara generados exitosamente.")

