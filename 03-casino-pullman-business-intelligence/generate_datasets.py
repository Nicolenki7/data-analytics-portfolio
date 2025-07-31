import pandas as pd
import numpy as np

np.random.seed(42)

# --- Dataset de Operaciones Hoteleras (simulado) ---
fechas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')

data_hotel = {
    'Fecha': fechas,
    'Ocupacion_Hotel': np.random.randint(50, 200, size=len(fechas)),
    'Ingresos_Hotel': np.random.uniform(5000, 25000, size=len(fechas)).round(2),
    'Huespedes_Registrados': np.random.randint(100, 500, size=len(fechas))
}
hotel_operations_df = pd.DataFrame(data_hotel)
hotel_operations_df.to_csv('/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/data/casino_hotel_operations_2023.csv', index=False)

# --- Dataset de Ingresos del Casino (simulado) ---
juegos = ['Tragamonedas', 'Ruleta', 'Blackjack', 'Poker']

data_casino = {
    'Fecha': pd.to_datetime(np.random.choice(fechas, size=3000)),
    'Juego': np.random.choice(juegos, size=3000),
    'Ingresos_Brutos': np.random.uniform(1000, 10000, size=3000).round(2),
    'Ganancia_Neta': np.random.uniform(500, 7000, size=3000).round(2)
}
casino_revenue_df = pd.DataFrame(data_casino)
casino_revenue_df.to_csv('/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/data/casino_revenue_2023.csv', index=False)

# --- Dataset de Demografía de Clientes (simulado) ---
edades = np.random.randint(20, 70, size=1000)
generos = np.random.choice(['Masculino', 'Femenino', 'Otro'], size=1000, p=[0.48, 0.48, 0.04])

data_clientes = {
    'ID_Cliente': range(1, 1001),
    'Edad': edades,
    'Genero': generos,
    'Ciudad_Origen': np.random.choice(['Rosario', 'Buenos Aires', 'Cordoba', 'Santa Fe', 'Otros'], size=1000),
    'Visitas_Casino': np.random.randint(1, 30, size=1000),
    'Gasto_Promedio_Casino': np.random.uniform(50, 1000, size=1000).round(2)
}
clientes_df = pd.DataFrame(data_clientes)
clientes_df.to_csv('/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/data/casino_clientes.csv', index=False)

print("Datasets simulados para Casino Pullman generados exitosamente.")

