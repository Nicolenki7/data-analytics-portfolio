#!/usr/bin/env python3
"""
Generador de datasets simulados para Hotel Rochavau - Portimão, Portugal
Datos realistas basados en patrones típicos de hoteles boutique en el Algarve
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configurar semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

def generate_occupancy_data():
    """Generar datos de ocupación diaria para 2023"""
    
    # Crear rango de fechas para 2023
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    data = []
    
    for date in dates:
        # Factores estacionales (Algarve tiene temporada alta en verano)
        month = date.month
        if month in [6, 7, 8, 9]:  # Temporada alta
            base_occupancy = 0.85
        elif month in [4, 5, 10]:  # Temporada media
            base_occupancy = 0.65
        else:  # Temporada baja
            base_occupancy = 0.45
        
        # Factor día de la semana (fines de semana más ocupados)
        weekday = date.weekday()
        if weekday in [4, 5, 6]:  # Viernes, Sábado, Domingo
            weekday_factor = 1.15
        else:
            weekday_factor = 0.95
        
        # Eventos especiales y festivales
        special_events = {
            (8, 15): 1.3,  # Festival de verano
            (12, 31): 1.25,  # Año nuevo
            (4, 25): 1.2,   # Día de la libertad (Portugal)
        }
        
        event_factor = special_events.get((month, date.day), 1.0)
        
        # Calcular ocupación con variabilidad aleatoria
        occupancy_rate = base_occupancy * weekday_factor * event_factor
        occupancy_rate += np.random.normal(0, 0.05)  # Variabilidad aleatoria
        occupancy_rate = max(0.1, min(1.0, occupancy_rate))  # Limitar entre 10% y 100%
        
        # Calcular habitaciones ocupadas (68 habitaciones total)
        rooms_occupied = int(68 * occupancy_rate)
        rooms_available = 68
        
        # ADR (Average Daily Rate) basado en temporada y ocupación
        if month in [6, 7, 8, 9]:
            base_adr = 120
        elif month in [4, 5, 10]:
            base_adr = 95
        else:
            base_adr = 75
        
        # Ajustar ADR por demanda
        demand_factor = 1 + (occupancy_rate - 0.7) * 0.3
        adr = base_adr * demand_factor * (1 + np.random.normal(0, 0.08))
        adr = max(60, min(200, adr))  # Limitar ADR
        
        # Calcular revenue
        revenue = rooms_occupied * adr
        revpar = revenue / rooms_available
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'rooms_available': rooms_available,
            'rooms_occupied': rooms_occupied,
            'occupancy_rate': round(occupancy_rate, 3),
            'adr': round(adr, 2),
            'revenue': round(revenue, 2),
            'revpar': round(revpar, 2),
            'day_of_week': date.strftime('%A'),
            'month': month,
            'season': 'High' if month in [6,7,8,9] else 'Medium' if month in [4,5,10] else 'Low'
        })
    
    return pd.DataFrame(data)

def generate_guest_reviews():
    """Generar datos de reseñas de huéspedes"""
    
    # Aspectos evaluados
    aspects = ['location', 'cleanliness', 'service', 'value', 'facilities', 'comfort']
    
    # Distribución de ratings (hotel de buena calidad)
    rating_weights = [0.02, 0.05, 0.15, 0.35, 0.43]  # Para ratings 1-5
    
    data = []
    
    for i in range(500):  # 500 reseñas
        # Fecha aleatoria en 2023
        review_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 364))
        
        # Rating general (1-5)
        overall_rating = np.random.choice([1, 2, 3, 4, 5], p=rating_weights)
        
        # Ratings por aspecto (correlacionados con rating general)
        aspect_ratings = {}
        for aspect in aspects:
            # Variación alrededor del rating general
            aspect_rating = overall_rating + np.random.normal(0, 0.5)
            aspect_rating = max(1, min(5, round(aspect_rating)))
            aspect_ratings[f'{aspect}_rating'] = aspect_rating
        
        # Tipo de viajero
        traveler_types = ['Couple', 'Family', 'Business', 'Solo', 'Friends']
        traveler_type = np.random.choice(traveler_types, p=[0.4, 0.25, 0.15, 0.1, 0.1])
        
        # Nacionalidad (típico para Algarve)
        nationalities = ['Portuguese', 'British', 'German', 'French', 'Spanish', 'Dutch', 'Other']
        nationality = np.random.choice(nationalities, p=[0.25, 0.20, 0.15, 0.12, 0.10, 0.08, 0.10])
        
        # Duración de estancia
        stay_duration = np.random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
                                       p=[0.05, 0.15, 0.20, 0.20, 0.15, 0.10, 0.08, 0.04, 0.02, 0.01])
        
        # Comentarios positivos/negativos basados en rating
        positive_comments = [
            "Great location near the beach", "Excellent staff", "Clean rooms", 
            "Beautiful pool area", "Good breakfast", "Comfortable beds"
        ]
        negative_comments = [
            "Room could be larger", "WiFi issues", "Noise from street", 
            "Limited parking", "Expensive drinks", "Slow check-in"
        ]
        
        if overall_rating >= 4:
            comments = random.sample(positive_comments, random.randint(1, 3))
        elif overall_rating <= 2:
            comments = random.sample(negative_comments, random.randint(1, 3))
        else:
            comments = random.sample(positive_comments + negative_comments, random.randint(1, 2))
        
        review_data = {
            'review_id': f'RV{i+1:04d}',
            'date': review_date.strftime('%Y-%m-%d'),
            'overall_rating': overall_rating,
            'traveler_type': traveler_type,
            'nationality': nationality,
            'stay_duration': stay_duration,
            'comments': '; '.join(comments),
            **aspect_ratings
        }
        
        data.append(review_data)
    
    return pd.DataFrame(data)

def generate_revenue_data():
    """Generar datos detallados de revenue por fuente"""
    
    # Crear datos mensuales para 2023
    months = pd.date_range('2023-01-01', '2023-12-31', freq='M')
    
    data = []
    
    for month in months:
        month_num = month.month
        
        # Revenue base según temporada
        if month_num in [6, 7, 8, 9]:
            base_revenue = 180000
        elif month_num in [4, 5, 10]:
            base_revenue = 120000
        else:
            base_revenue = 80000
        
        # Distribución por canal
        direct_bookings = base_revenue * 0.35 * (1 + np.random.normal(0, 0.1))
        booking_com = base_revenue * 0.25 * (1 + np.random.normal(0, 0.1))
        expedia = base_revenue * 0.15 * (1 + np.random.normal(0, 0.1))
        airbnb = base_revenue * 0.10 * (1 + np.random.normal(0, 0.1))
        other_otas = base_revenue * 0.15 * (1 + np.random.normal(0, 0.1))
        
        # Revenue adicional (servicios)
        restaurant_revenue = base_revenue * 0.12 * (1 + np.random.normal(0, 0.15))
        bar_revenue = base_revenue * 0.08 * (1 + np.random.normal(0, 0.15))
        spa_revenue = base_revenue * 0.05 * (1 + np.random.normal(0, 0.2))
        parking_revenue = base_revenue * 0.03 * (1 + np.random.normal(0, 0.1))
        
        total_room_revenue = direct_bookings + booking_com + expedia + airbnb + other_otas
        total_ancillary_revenue = restaurant_revenue + bar_revenue + spa_revenue + parking_revenue
        total_revenue = total_room_revenue + total_ancillary_revenue
        
        data.append({
            'month': month.strftime('%Y-%m'),
            'direct_bookings': round(direct_bookings, 2),
            'booking_com': round(booking_com, 2),
            'expedia': round(expedia, 2),
            'airbnb': round(airbnb, 2),
            'other_otas': round(other_otas, 2),
            'total_room_revenue': round(total_room_revenue, 2),
            'restaurant_revenue': round(restaurant_revenue, 2),
            'bar_revenue': round(bar_revenue, 2),
            'spa_revenue': round(spa_revenue, 2),
            'parking_revenue': round(parking_revenue, 2),
            'total_ancillary_revenue': round(total_ancillary_revenue, 2),
            'total_revenue': round(total_revenue, 2),
            'season': 'High' if month_num in [6,7,8,9] else 'Medium' if month_num in [4,5,10] else 'Low'
        })
    
    return pd.DataFrame(data)

def main():
    """Generar todos los datasets"""
    
    print("Generando datasets para Hotel Rochavau...")
    
    # Generar datasets
    occupancy_df = generate_occupancy_data()
    reviews_df = generate_guest_reviews()
    revenue_df = generate_revenue_data()
    
    # Guardar datasets
    occupancy_df.to_csv('data/hotel_occupancy_2023.csv', index=False)
    reviews_df.to_csv('data/guest_reviews.csv', index=False)
    revenue_df.to_csv('data/revenue_data.csv', index=False)
    
    print("✅ Datasets generados exitosamente:")
    print(f"   - hotel_occupancy_2023.csv: {len(occupancy_df)} registros")
    print(f"   - guest_reviews.csv: {len(reviews_df)} registros")
    print(f"   - revenue_data.csv: {len(revenue_df)} registros")
    
    # Mostrar estadísticas básicas
    print("\n📊 Estadísticas básicas:")
    print(f"   - Ocupación promedio: {occupancy_df['occupancy_rate'].mean():.1%}")
    print(f"   - ADR promedio: €{occupancy_df['adr'].mean():.2f}")
    print(f"   - RevPAR promedio: €{occupancy_df['revpar'].mean():.2f}")
    print(f"   - Rating promedio: {reviews_df['overall_rating'].mean():.1f}/5")
    print(f"   - Revenue anual total: €{revenue_df['total_revenue'].sum():,.0f}")

if __name__ == "__main__":
    main()

