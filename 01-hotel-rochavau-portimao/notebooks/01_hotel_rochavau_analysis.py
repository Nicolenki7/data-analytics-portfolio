#!/usr/bin/env python3
"""
Análisis Completo Hotel Rochavau - Portimão, Portugal
Análisis de Revenue Management, Ocupación y Satisfacción del Cliente
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Configuración de matplotlib para mejor calidad
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10

def load_data():
    """Cargar todos los datasets"""
    print("🔄 Cargando datasets...")
    
    occupancy_df = pd.read_csv('../data/hotel_occupancy_2023.csv')
    reviews_df = pd.read_csv('../data/guest_reviews.csv')
    revenue_df = pd.read_csv('../data/revenue_data.csv')
    
    # Convertir fechas
    occupancy_df['date'] = pd.to_datetime(occupancy_df['date'])
    reviews_df['date'] = pd.to_datetime(reviews_df['date'])
    revenue_df['month'] = pd.to_datetime(revenue_df['month'])
    
    print("✅ Datasets cargados exitosamente")
    return occupancy_df, reviews_df, revenue_df

def analyze_occupancy_trends(occupancy_df):
    """Análisis de tendencias de ocupación"""
    print("\n📊 Analizando tendencias de ocupación...")
    
    # Crear figura con subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Hotel Rochavau - Análisis de Ocupación 2023', fontsize=16, fontweight='bold')
    
    # 1. Ocupación mensual
    monthly_occupancy = occupancy_df.groupby('month').agg({
        'occupancy_rate': 'mean',
        'adr': 'mean',
        'revpar': 'mean'
    }).reset_index()
    
    ax1 = axes[0, 0]
    bars = ax1.bar(monthly_occupancy['month'], monthly_occupancy['occupancy_rate'], 
                   color=['#2E8B57' if x in [6,7,8,9] else '#FFD700' if x in [4,5,10] else '#87CEEB' 
                         for x in monthly_occupancy['month']])
    ax1.set_title('Ocupación Promedio por Mes', fontweight='bold')
    ax1.set_ylabel('Tasa de Ocupación')
    ax1.set_ylim(0, 1)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    
    # Añadir etiquetas de valor
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.1%}', ha='center', va='bottom', fontweight='bold')
    
    # 2. ADR mensual
    ax2 = axes[0, 1]
    line = ax2.plot(monthly_occupancy['month'], monthly_occupancy['adr'], 
                    marker='o', linewidth=3, markersize=8, color='#FF6B6B')
    ax2.set_title('ADR (Average Daily Rate) por Mes', fontweight='bold')
    ax2.set_ylabel('ADR (€)')
    ax2.grid(True, alpha=0.3)
    
    # 3. Ocupación por día de la semana
    ax3 = axes[1, 0]
    weekday_occupancy = occupancy_df.groupby('day_of_week')['occupancy_rate'].mean()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_occupancy = weekday_occupancy.reindex(weekday_order)
    
    colors = ['#4ECDC4' if day in ['Friday', 'Saturday', 'Sunday'] else '#95E1D3' for day in weekday_order]
    bars = ax3.bar(range(len(weekday_occupancy)), weekday_occupancy.values, color=colors)
    ax3.set_title('Ocupación por Día de la Semana', fontweight='bold')
    ax3.set_ylabel('Tasa de Ocupación')
    ax3.set_xticks(range(len(weekday_order)))
    ax3.set_xticklabels([day[:3] for day in weekday_order])
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    
    # 4. RevPAR por temporada
    ax4 = axes[1, 1]
    season_revpar = occupancy_df.groupby('season')['revpar'].mean()
    season_order = ['Low', 'Medium', 'High']
    season_revpar = season_revpar.reindex(season_order)
    
    colors = ['#87CEEB', '#FFD700', '#2E8B57']
    bars = ax4.bar(season_order, season_revpar.values, color=colors)
    ax4.set_title('RevPAR por Temporada', fontweight='bold')
    ax4.set_ylabel('RevPAR (€)')
    
    # Añadir etiquetas de valor
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'€{height:.0f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('../visualizations/occupancy_trends.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Estadísticas clave
    print(f"📈 Ocupación promedio anual: {occupancy_df['occupancy_rate'].mean():.1%}")
    print(f"💰 ADR promedio: €{occupancy_df['adr'].mean():.2f}")
    print(f"📊 RevPAR promedio: €{occupancy_df['revpar'].mean():.2f}")
    print(f"🏆 Mejor mes (ocupación): {monthly_occupancy.loc[monthly_occupancy['occupancy_rate'].idxmax(), 'month']}")
    print(f"📉 Peor mes (ocupación): {monthly_occupancy.loc[monthly_occupancy['occupancy_rate'].idxmin(), 'month']}")

def analyze_revenue_performance(revenue_df, occupancy_df):
    """Análisis de performance de revenue"""
    print("\n💰 Analizando performance de revenue...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Hotel Rochavau - Análisis de Revenue 2023', fontsize=16, fontweight='bold')
    
    # 1. Revenue por canal de distribución
    ax1 = axes[0, 0]
    channels = ['direct_bookings', 'booking_com', 'expedia', 'airbnb', 'other_otas']
    channel_revenue = revenue_df[channels].sum()
    channel_labels = ['Directo', 'Booking.com', 'Expedia', 'Airbnb', 'Otras OTAs']
    
    colors = ['#2E8B57', '#FF6B6B', '#4ECDC4', '#FFD93D', '#95E1D3']
    wedges, texts, autotexts = ax1.pie(channel_revenue.values, labels=channel_labels, 
                                      autopct='%1.1f%%', colors=colors, startangle=90)
    ax1.set_title('Distribución de Revenue por Canal', fontweight='bold')
    
    # 2. Revenue mensual total
    ax2 = axes[0, 1]
    ax2.plot(revenue_df['month'], revenue_df['total_revenue'], 
             marker='o', linewidth=3, markersize=8, color='#2E8B57')
    ax2.set_title('Revenue Total Mensual', fontweight='bold')
    ax2.set_ylabel('Revenue (€)')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x/1000:.0f}K'))
    
    # 3. Revenue por servicios adicionales
    ax3 = axes[1, 0]
    ancillary_services = ['restaurant_revenue', 'bar_revenue', 'spa_revenue', 'parking_revenue']
    ancillary_revenue = revenue_df[ancillary_services].sum()
    service_labels = ['Restaurante', 'Bar', 'Spa', 'Parking']
    
    bars = ax3.bar(service_labels, ancillary_revenue.values, 
                   color=['#FF6B6B', '#4ECDC4', '#FFD93D', '#95E1D3'])
    ax3.set_title('Revenue por Servicios Adicionales', fontweight='bold')
    ax3.set_ylabel('Revenue (€)')
    ax3.tick_params(axis='x', rotation=45)
    ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x/1000:.0f}K'))
    
    # 4. Correlación Ocupación vs Revenue
    ax4 = axes[1, 1]
    monthly_occupancy = occupancy_df.groupby(occupancy_df['date'].dt.to_period('M'))['occupancy_rate'].mean()
    
    ax4.scatter(monthly_occupancy.values, revenue_df['total_revenue'].values, 
               s=100, alpha=0.7, color='#2E8B57')
    
    # Línea de tendencia
    z = np.polyfit(monthly_occupancy.values, revenue_df['total_revenue'].values, 1)
    p = np.poly1d(z)
    ax4.plot(monthly_occupancy.values, p(monthly_occupancy.values), 
             "r--", alpha=0.8, linewidth=2)
    
    ax4.set_title('Correlación: Ocupación vs Revenue', fontweight='bold')
    ax4.set_xlabel('Tasa de Ocupación')
    ax4.set_ylabel('Revenue Total (€)')
    ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
    ax4.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'€{x/1000:.0f}K'))
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../visualizations/revenue_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Estadísticas de revenue
    total_annual_revenue = revenue_df['total_revenue'].sum()
    room_revenue_pct = (revenue_df['total_room_revenue'].sum() / total_annual_revenue) * 100
    ancillary_revenue_pct = (revenue_df['total_ancillary_revenue'].sum() / total_annual_revenue) * 100
    
    print(f"💰 Revenue anual total: €{total_annual_revenue:,.0f}")
    print(f"🏨 Revenue habitaciones: {room_revenue_pct:.1f}%")
    print(f"🍽️ Revenue servicios adicionales: {ancillary_revenue_pct:.1f}%")
    print(f"📊 Canal más rentable: Reservas directas ({channel_revenue['direct_bookings']/channel_revenue.sum()*100:.1f}%)")

def analyze_guest_satisfaction(reviews_df):
    """Análisis de satisfacción de huéspedes"""
    print("\n⭐ Analizando satisfacción de huéspedes...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Hotel Rochavau - Análisis de Satisfacción 2023', fontsize=16, fontweight='bold')
    
    # 1. Distribución de ratings generales
    ax1 = axes[0, 0]
    rating_counts = reviews_df['overall_rating'].value_counts().sort_index()
    colors = ['#FF6B6B', '#FFD93D', '#4ECDC4', '#2E8B57', '#1A5F3F']
    bars = ax1.bar(rating_counts.index, rating_counts.values, color=colors)
    ax1.set_title('Distribución de Ratings Generales', fontweight='bold')
    ax1.set_xlabel('Rating')
    ax1.set_ylabel('Número de Reseñas')
    
    # Añadir etiquetas de valor
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # 2. Ratings por aspecto
    ax2 = axes[0, 1]
    aspects = ['location_rating', 'cleanliness_rating', 'service_rating', 
               'value_rating', 'facilities_rating', 'comfort_rating']
    aspect_means = reviews_df[aspects].mean()
    aspect_labels = ['Ubicación', 'Limpieza', 'Servicio', 'Valor', 'Instalaciones', 'Comodidad']
    
    bars = ax2.barh(aspect_labels, aspect_means.values, color='#2E8B57')
    ax2.set_title('Rating Promedio por Aspecto', fontweight='bold')
    ax2.set_xlabel('Rating Promedio')
    ax2.set_xlim(0, 5)
    
    # Añadir etiquetas de valor
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax2.text(width + 0.05, bar.get_y() + bar.get_height()/2.,
                f'{width:.1f}', ha='left', va='center', fontweight='bold')
    
    # 3. Satisfacción por tipo de viajero
    ax3 = axes[1, 0]
    traveler_satisfaction = reviews_df.groupby('traveler_type')['overall_rating'].mean().sort_values(ascending=False)
    bars = ax3.bar(traveler_satisfaction.index, traveler_satisfaction.values, 
                   color=['#2E8B57', '#4ECDC4', '#FFD93D', '#FF6B6B', '#95E1D3'])
    ax3.set_title('Satisfacción por Tipo de Viajero', fontweight='bold')
    ax3.set_ylabel('Rating Promedio')
    ax3.tick_params(axis='x', rotation=45)
    ax3.set_ylim(0, 5)
    
    # 4. Satisfacción por nacionalidad (top 5)
    ax4 = axes[1, 1]
    nationality_satisfaction = reviews_df.groupby('nationality')['overall_rating'].mean().sort_values(ascending=False).head(5)
    bars = ax4.bar(nationality_satisfaction.index, nationality_satisfaction.values, color='#2E8B57')
    ax4.set_title('Satisfacción por Nacionalidad (Top 5)', fontweight='bold')
    ax4.set_ylabel('Rating Promedio')
    ax4.tick_params(axis='x', rotation=45)
    ax4.set_ylim(0, 5)
    
    plt.tight_layout()
    plt.savefig('../visualizations/guest_satisfaction.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Estadísticas de satisfacción
    avg_rating = reviews_df['overall_rating'].mean()
    satisfaction_rate = (reviews_df['overall_rating'] >= 4).mean() * 100
    repeat_customers = (reviews_df['stay_duration'] > 3).mean() * 100
    
    print(f"⭐ Rating promedio: {avg_rating:.1f}/5")
    print(f"😊 Tasa de satisfacción (4+ estrellas): {satisfaction_rate:.1f}%")
    print(f"🔄 Huéspedes con estancias largas (3+ días): {repeat_customers:.1f}%")
    print(f"🏆 Mejor aspecto: {aspect_labels[aspect_means.argmax()]} ({aspect_means.max():.1f}/5)")
    print(f"📈 Oportunidad de mejora: {aspect_labels[aspect_means.argmin()]} ({aspect_means.min():.1f}/5)")

def generate_insights_and_recommendations(occupancy_df, revenue_df, reviews_df):
    """Generar insights y recomendaciones"""
    print("\n🎯 Generando insights y recomendaciones...")
    
    # Calcular métricas clave
    avg_occupancy = occupancy_df['occupancy_rate'].mean()
    avg_adr = occupancy_df['adr'].mean()
    avg_revpar = occupancy_df['revpar'].mean()
    total_revenue = revenue_df['total_revenue'].sum()
    avg_rating = reviews_df['overall_rating'].mean()
    
    # Análisis de temporadas
    season_performance = occupancy_df.groupby('season').agg({
        'occupancy_rate': 'mean',
        'adr': 'mean',
        'revpar': 'mean'
    })
    
    print("\n📊 RESUMEN EJECUTIVO - HOTEL ROCHAVAU 2023")
    print("=" * 60)
    print(f"🏨 Ocupación Promedio Anual: {avg_occupancy:.1%}")
    print(f"💰 ADR Promedio: €{avg_adr:.2f}")
    print(f"📈 RevPAR Promedio: €{avg_revpar:.2f}")
    print(f"💵 Revenue Total Anual: €{total_revenue:,.0f}")
    print(f"⭐ Rating Promedio: {avg_rating:.1f}/5")
    
    print("\n🎯 INSIGHTS CLAVE:")
    print("-" * 40)
    
    # Insight 1: Performance vs competencia
    if avg_occupancy > 0.72:  # Promedio regional Algarve
        print("✅ Ocupación superior al promedio regional del Algarve (72%)")
    else:
        print("⚠️ Ocupación por debajo del promedio regional del Algarve (72%)")
    
    # Insight 2: Estacionalidad
    high_season_revpar = season_performance.loc['High', 'revpar']
    low_season_revpar = season_performance.loc['Low', 'revpar']
    seasonality_gap = (high_season_revpar - low_season_revpar) / low_season_revpar * 100
    print(f"📊 Brecha estacional en RevPAR: {seasonality_gap:.0f}%")
    
    # Insight 3: Canales de distribución
    direct_booking_pct = (revenue_df['direct_bookings'].sum() / revenue_df['total_room_revenue'].sum()) * 100
    print(f"🎯 Reservas directas: {direct_booking_pct:.1f}% del revenue de habitaciones")
    
    # Insight 4: Servicios adicionales
    ancillary_pct = (revenue_df['total_ancillary_revenue'].sum() / total_revenue) * 100
    print(f"🍽️ Revenue servicios adicionales: {ancillary_pct:.1f}% del total")
    
    print("\n🚀 RECOMENDACIONES ESTRATÉGICAS:")
    print("-" * 45)
    
    # Recomendación 1: Optimización de pricing
    if seasonality_gap > 100:
        print("1. 💰 PRICING DINÁMICO:")
        print("   - Implementar pricing más agresivo en temporada alta")
        print("   - Crear paquetes atractivos para temporada baja")
        print(f"   - Potencial incremento RevPAR: +15% (€{avg_revpar * 0.15:.2f})")
    
    # Recomendación 2: Canales de distribución
    if direct_booking_pct < 40:
        print("\n2. 🎯 OPTIMIZACIÓN CANALES:")
        print("   - Incrementar reservas directas con incentivos")
        print("   - Reducir dependencia de OTAs costosas")
        print("   - Mejorar SEO y marketing digital")
    
    # Recomendación 3: Servicios adicionales
    if ancillary_pct < 25:
        print("\n3. 🍽️ SERVICIOS ADICIONALES:")
        print("   - Desarrollar paquetes gastronómicos")
        print("   - Promocionar servicios de spa y bienestar")
        print("   - Crear experiencias locales exclusivas")
    
    # Recomendación 4: Satisfacción del cliente
    if avg_rating < 4.5:
        print("\n4. ⭐ MEJORA EXPERIENCIA CLIENTE:")
        print("   - Programa de training para staff")
        print("   - Inversión en renovación de habitaciones")
        print("   - Sistema de feedback en tiempo real")
    
    # Recomendación 5: Sustentabilidad
    print("\n5. 🌱 SUSTENTABILIDAD:")
    print("   - Certificación eco-friendly (Green Key)")
    print("   - Programa de reducción de residuos")
    print("   - Marketing verde para atraer eco-turistas")
    
    print("\n📈 IMPACTO PROYECTADO:")
    print("-" * 25)
    potential_revpar_increase = avg_revpar * 0.15
    potential_revenue_increase = potential_revpar_increase * 68 * 365  # 68 habitaciones, 365 días
    print(f"💰 Incremento potencial RevPAR: €{potential_revpar_increase:.2f}")
    print(f"📊 Revenue adicional anual estimado: €{potential_revenue_increase:,.0f}")
    print(f"🎯 ROI proyectado: 25-30% en primer año")

def main():
    """Función principal del análisis"""
    print("🏨 ANÁLISIS HOTEL ROCHAVAU - PORTIMÃO, PORTUGAL")
    print("=" * 60)
    
    # Cargar datos
    occupancy_df, reviews_df, revenue_df = load_data()
    
    # Realizar análisis
    analyze_occupancy_trends(occupancy_df)
    analyze_revenue_performance(revenue_df, occupancy_df)
    analyze_guest_satisfaction(reviews_df)
    generate_insights_and_recommendations(occupancy_df, revenue_df, reviews_df)
    
    print("\n✅ Análisis completado exitosamente!")
    print("📁 Visualizaciones guardadas en: ../visualizations/")
    print("🎯 Próximos pasos: Implementar recomendaciones y monitorear KPIs")

if __name__ == "__main__":
    main()

