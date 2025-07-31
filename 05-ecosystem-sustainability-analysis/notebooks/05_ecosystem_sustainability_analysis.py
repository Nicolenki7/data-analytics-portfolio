
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datasets
agua_df = pd.read_csv("/home/ubuntu/data-analytics-portfolio/05-ecosystem-sustainability-analysis/data/ecosystem_agua_2023.csv")
biodiversidad_df = pd.read_csv("/home/ubuntu/data-analytics-portfolio/05-ecosystem-sustainability-analysis/data/ecosystem_biodiversidad_2023.csv")

# Convertir la columna de fecha a formato datetime
agua_df["Fecha"] = pd.to_datetime(agua_df["Fecha"])
biodiversidad_df["Fecha"] = pd.to_datetime(biodiversidad_df["Fecha"])

# --- Análisis de Calidad del Agua ---
# Tendencia de pH del Agua
plt.figure(figsize=(12, 6))
sns.lineplot(x="Fecha", y="pH", data=agua_df)
plt.title("Tendencia Diaria del pH del Agua (2023)")
plt.xlabel("Fecha")
plt.ylabel("pH")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("/home/ubuntu/data-analytics-portfolio/05-ecosystem-sustainability-analysis/visualizations/water_ph_trend.png")
plt.close()

# Distribución de Oxígeno Disuelto
plt.figure(figsize=(8, 5))
sns.histplot(agua_df["Oxigeno_Disuelto_mgL"], bins=15, kde=True)
plt.title("Distribución de Oxígeno Disuelto en el Agua (mg/L)")
plt.xlabel("Oxígeno Disuelto (mg/L)")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.savefig("/home/ubuntu/data-analytics-portfolio/05-ecosystem-sustainability-analysis/visualizations/dissolved_oxygen_distribution.png")
plt.close()

# --- Análisis de Biodiversidad ---
# Conteo de Especies por Ubicación
conteo_ubicacion = biodiversidad_df.groupby("Ubicacion")["Conteo"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=conteo_ubicacion.index, y=conteo_ubicacion.values, palette="Greens")
plt.title("Conteo Total de Especies por Ubicación (2023)")
plt.xlabel("Ubicación")
plt.ylabel("Conteo de Especies")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("/home/ubuntu/data-analytics-portfolio/05-ecosystem-sustainability-analysis/visualizations/species_count_by_location.png")
plt.close()

# Especies más Comunes
especies_comunes = biodiversidad_df["Especie"].value_counts().head(5)

plt.figure(figsize=(10, 6))
sns.barplot(x=especies_comunes.index, y=especies_comunes.values, palette="Blues")
plt.title("Top 5 Especies Más Comunes (2023)")
plt.xlabel("Especie")
plt.ylabel("Número de Observaciones")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("/home/ubuntu/data-analytics-portfolio/05-ecosystem-sustainability-analysis/visualizations/top_species.png")
plt.close()

print("Análisis y visualizaciones para Ecosystem Sustainability generados exitosamente.")


