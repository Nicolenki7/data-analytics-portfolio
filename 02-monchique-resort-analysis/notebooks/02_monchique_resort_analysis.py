
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datasets
hotel_occupancy_df = pd.read_csv("/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/data/monchique_hotel_occupancy_2023.csv")
spa_services_df = pd.read_csv("/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/data/monchique_spa_services.csv")
guest_reviews_df = pd.read_csv("/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/data/monchique_guest_reviews.csv")

# Convertir la columna de fecha a formato datetime
hotel_occupancy_df["Fecha"] = pd.to_datetime(hotel_occupancy_df["Fecha"])
spa_services_df["Fecha"] = pd.to_datetime(spa_services_df["Fecha"])
guest_reviews_df["Fecha_Estancia"] = pd.to_datetime(guest_reviews_df["Fecha_Estancia"])

# --- Análisis de Ocupación y Revenue ---
# Calcular la tasa de ocupación
hotel_occupancy_df["Tasa_Ocupacion"] = (hotel_occupancy_df["Habitaciones_Ocupadas"] / hotel_occupancy_df["Habitaciones_Disponibles"]) * 100

# Tendencia de Ocupación Mensual
hotel_occupancy_df["Mes"] = hotel_occupancy_df["Fecha"].dt.month
ocupacion_mensual = hotel_occupancy_df.groupby("Mes")["Tasa_Ocupacion"].mean()

plt.figure(figsize=(10, 6))
sns.lineplot(x=ocupacion_mensual.index, y=ocupacion_mensual.values)
plt.title("Tendencia Mensual de Tasa de Ocupación en Monchique Resort (2023)")
plt.xlabel("Mes")
plt.ylabel("Tasa de Ocupación (%)")
plt.grid(True)
plt.savefig("/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/visualizations/monchique_occupancy_trend.png")
plt.close()

# Distribución de ADR
plt.figure(figsize=(10, 6))
sns.histplot(hotel_occupancy_df["ADR"], bins=30, kde=True)
plt.title("Distribución del ADR (Average Daily Rate) en Monchique Resort (2023)")
plt.xlabel("ADR (€)")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.savefig("/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/visualizations/monchique_adr_distribution.png")
plt.close()

# --- Análisis de Servicios de Spa ---
# Ingresos por Servicio de Spa
ingresos_spa_servicio = spa_services_df.groupby("Servicio")["Ingresos"].sum().sort_values(ascending=False)

plt.figure(figsize=(12, 7))
sns.barplot(x=ingresos_spa_servicio.index, y=ingresos_spa_servicio.values, palette="viridis")
plt.title("Ingresos Totales por Servicio de Spa en Monchique Resort (2023)")
plt.xlabel("Servicio de Spa")
plt.ylabel("Ingresos Totales (€)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/visualizations/monchique_spa_revenue.png")
plt.close()

# Duración promedio de servicios de spa
duracion_promedio_spa = spa_services_df.groupby("Servicio")["Duracion_Minutos"].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 7))
sns.barplot(x=duracion_promedio_spa.index, y=duracion_promedio_spa.values, palette="magma")
plt.title("Duración Promedio por Servicio de Spa en Monchique Resort (2023)")
plt.xlabel("Servicio de Spa")
plt.ylabel("Duración Promedio (Minutos)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/visualizations/monchique_spa_duration.png")
plt.close()

# --- Análisis de Satisfacción del Cliente ---
# Distribución de Ratings Generales
plt.figure(figsize=(8, 5))
sns.countplot(x="Rating_General", data=guest_reviews_df, palette="coolwarm")
plt.title("Distribución de Ratings Generales de Huespedes en Monchique Resort (2023)")
plt.xlabel("Rating General (1-5)")
plt.ylabel("Número de Reseñas")
plt.savefig("/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/visualizations/monchique_guest_ratings.png")
plt.close()

# Correlación entre Ratings y Comentarios Positivos/Negativos
ratings_correlation = guest_reviews_df[["Rating_General", "Rating_Servicio", "Rating_Instalaciones", "Comentario_Positivo", "Comentario_Negativo"]].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(ratings_correlation, annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Matriz de Correlación de Ratings y Comentarios en Monchique Resort")
plt.tight_layout()
plt.savefig("/home/ubuntu/data-analytics-portfolio/02-monchique-resort-analysis/visualizations/monchique_ratings_correlation.png")
plt.close()

print("Análisis y visualizaciones para Monchique Resort generados exitosamente.")


