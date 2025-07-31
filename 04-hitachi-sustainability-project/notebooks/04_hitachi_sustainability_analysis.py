
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datasets
energia_df = pd.read_csv("/home/ubuntu/data-analytics-portfolio/04-hitachi-sustainability-project/data/hitachi_energia_2023.csv")
emisiones_co2_df = pd.read_csv("/home/ubuntu/data-analytics-portfolio/04-hitachi-sustainability-project/data/hitachi_emisiones_co2_2023.csv")

# Convertir la columna de fecha a formato datetime
energia_df["Timestamp"] = pd.to_datetime(energia_df["Timestamp"])
emisiones_co2_df["Timestamp"] = pd.to_datetime(emisiones_co2_df["Timestamp"])

# --- Análisis de Consumo Energético ---
# Consumo Energético Diario Promedio
energia_df["Fecha"] = energia_df["Timestamp"].dt.date
consumo_diario = energia_df.groupby("Fecha")["Consumo_kWh"].sum()

plt.figure(figsize=(12, 6))
sns.lineplot(x=consumo_diario.index, y=consumo_diario.values)
plt.title("Consumo Energético Diario Total (Hitachi Vantara, 2023)")
plt.xlabel("Fecha")
plt.ylabel("Consumo de Energía (kWh)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("/home/ubuntu/data-analytics-portfolio/04-hitachi-sustainability-project/visualizations/hitachi_daily_energy_consumption.png")
plt.close()

# Correlación entre Consumo y Temperatura
plt.figure(figsize=(8, 6))
sns.scatterplot(x="Temperatura_C", y="Consumo_kWh", data=energia_df, alpha=0.6)
plt.title("Correlación entre Consumo Energético y Temperatura (Hitachi Vantara)")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Consumo de Energía (kWh)")
plt.grid(True)
plt.savefig("/home/ubuntu/data-analytics-portfolio/04-hitachi-sustainability-project/visualizations/hitachi_energy_temp_correlation.png")
plt.close()

# --- Análisis de Emisiones de CO2 ---
# Emisiones de CO2 por Fuente
emisiones_fuente = emisiones_co2_df.groupby("Fuente_Emision")["Emisiones_CO2_ton"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x=emisiones_fuente.index, y=emisiones_fuente.values, palette="Reds")
plt.title("Emisiones de CO2 por Fuente (Hitachi Vantara, 2023)")
plt.xlabel("Fuente de Emisión")
plt.ylabel("Emisiones de CO2 (toneladas)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("/home/ubuntu/data-analytics-portfolio/04-hitachi-sustainability-project/visualizations/hitachi_co2_emissions_by_source.png")
plt.close()

# Tendencia de Emisiones de CO2 Mensual
emisiones_co2_df["Mes"] = emisiones_co2_df["Timestamp"].dt.month
emisiones_mensuales = emisiones_co2_df.groupby("Mes")["Emisiones_CO2_ton"].sum()

plt.figure(figsize=(10, 6))
sns.lineplot(x=emisiones_mensuales.index, y=emisiones_mensuales.values)
plt.title("Tendencia Mensual de Emisiones de CO2 (Hitachi Vantara, 2023)")
plt.xlabel("Mes")
plt.ylabel("Emisiones de CO2 (toneladas)")
plt.grid(True)
plt.savefig("/home/ubuntu/data-analytics-portfolio/04-hitachi-sustainability-project/visualizations/hitachi_monthly_co2_emissions.png")
plt.close()

print("Análisis y visualizaciones para Hitachi Vantara generados exitosamente.")


