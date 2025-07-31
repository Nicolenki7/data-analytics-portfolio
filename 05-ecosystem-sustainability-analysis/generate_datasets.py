import pandas as pd
import numpy as np

np.random.seed(42)

# --- Dataset de Calidad del Agua (simulado) ---
fechas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')

data_agua = {
    'Fecha': fechas,
    'pH': np.random.uniform(6.5, 8.5, size=len(fechas)).round(2),
    'Oxigeno_Disuelto_mgL': np.random.uniform(5, 10, size=len(fechas)).round(2),
    'Turbidez_NTU': np.random.uniform(1, 50, size=len(fechas)).round(2),
    'Temperatura_Agua_C': np.random.uniform(10, 30, size=len(fechas)).round(2)
}
agua_df = pd.DataFrame(data_agua)
agua_df.to_csv('/home/ubuntu/data-analytics-portfolio/05-ecosystem-sustainability-analysis/data/ecosystem_agua_2023.csv', index=False)

# --- Dataset de Biodiversidad (simulado) ---
especies = ['Pez A', 'Pez B', 'Ave C', 'Insecto D', 'Planta E']

data_biodiversidad = {
    'Fecha': pd.to_datetime(np.random.choice(fechas, size=1000)),
    'Especie': np.random.choice(especies, size=1000),
    'Conteo': np.random.randint(1, 100, size=1000),
    'Ubicacion': np.random.choice(['Bosque', 'Rio', 'Lago', 'Montaña'], size=1000)
}
biodiversidad_df = pd.DataFrame(data_biodiversidad)
biodiversidad_df.to_csv('/home/ubuntu/data-analytics-portfolio/05-ecosystem-sustainability-analysis/data/ecosystem_biodiversidad_2023.csv', index=False)

print("Datasets simulados para Ecosystem Sustainability generados exitosamente.")
