
import pandas as pd
import numpy as np

# Seed para reproducibilidad
np.random.seed(42)

# --- Dataset de Ocupación y Revenue (simulado) ---
fechas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')

data_ocupacion = {
    'Fecha': fechas,
    'Habitaciones_Disponibles': 200, # Resort de 200 habitaciones
    'Habitaciones_Ocupadas': np.random.randint(80, 190, size=len(fechas)),
    'ADR': np.random.uniform(250, 600, size=len(fechas)).round(2), # Average Daily Rate en euros
    'RevPAR': np.random.uniform(150, 550, size=len(fechas)).round(2) # Revenue per Available Room
}
hotel_occupancy_df = pd.DataFrame(data_ocupacion)

# Ajustar RevPAR para que sea coherente con Ocupación y ADR
hotel_occupancy_df['RevPAR'] = (hotel_occupancy_df['Habitaciones_Ocupadas'] / hotel_occupancy_df['Habitaciones_Disponibles'] * hotel_occupancy_df['ADR']).round(2)

hotel_occupancy_df.to_csv('/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/data/monchique_hotel_occupancy_2023.csv', index=False)

# --- Dataset de Servicios de Spa (simulado) ---
servicios_spa = ['Masaje Relajante', 'Tratamiento Facial', 'Envoltura Corporal', 'Hidroterapia', 'Manicura/Pedicura']

data_spa = {
    'Fecha': pd.to_datetime(np.random.choice(fechas, size=1000)),
    'Servicio': np.random.choice(servicios_spa, size=1000),
    'Ingresos': np.random.uniform(50, 300, size=1000).round(2),
    'Duracion_Minutos': np.random.randint(30, 120, size=1000)
}
spa_services_df = pd.DataFrame(data_spa)
spa_services_df.to_csv('/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/data/monchique_spa_services.csv', index=False)

# --- Dataset de Satisfacción del Cliente (simulado) ---
ratings = [1, 2, 3, 4, 5]

data_reviews = {
    'ID_Huesped': range(1, 1501),
    'Fecha_Estancia': pd.to_datetime(np.random.choice(fechas, size=1500)),
    'Rating_General': np.random.choice(ratings, size=1500, p=[0.05, 0.05, 0.1, 0.3, 0.5]),
    'Rating_Servicio': np.random.choice(ratings, size=1500, p=[0.05, 0.05, 0.1, 0.3, 0.5]),
    'Rating_Instalaciones': np.random.choice(ratings, size=1500, p=[0.05, 0.05, 0.1, 0.3, 0.5]),
    'Comentario_Positivo': np.random.choice([True, False], size=1500, p=[0.7, 0.3]),
    'Comentario_Negativo': np.random.choice([True, False], size=1500, p=[0.3, 0.7])
}
guest_reviews_df = pd.DataFrame(data_reviews)
guest_reviews_df.to_csv('/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/data/monchique_guest_reviews.csv', index=False)

print("Datasets simulados para Monchique Resort generados exitosamente.")


