
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datasets
hotel_operations_df = pd.read_csv("/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/data/casino_hotel_operations_2023.csv")
casino_revenue_df = pd.read_csv("/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/data/casino_revenue_2023.csv")
clientes_df = pd.read_csv("/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/data/casino_clientes.csv")

# Convertir la columna de fecha a formato datetime
hotel_operations_df["Fecha"] = pd.to_datetime(hotel_operations_df["Fecha"])
casino_revenue_df["Fecha"] = pd.to_datetime(casino_revenue_df["Fecha"])

# --- Análisis de Operaciones Hoteleras ---
# Tendencia de Ocupación Hotelera Mensual
hotel_operations_df["Mes"] = hotel_operations_df["Fecha"].dt.month
ocupacion_hotel_mensual = hotel_operations_df.groupby("Mes")["Ocupacion_Hotel"].mean()

plt.figure(figsize=(10, 6))
sns.lineplot(x=ocupacion_hotel_mensual.index, y=ocupacion_hotel_mensual.values)
plt.title("Tendencia Mensual de Ocupación Hotelera (Casino Pullman, 2023)")
plt.xlabel("Mes")
plt.ylabel("Ocupación Promedio")
plt.grid(True)
plt.savefig("/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/visualizations/hotel_occupancy_trend.png")
plt.close()

# Ingresos Hoteleros Mensuales
ingresos_hotel_mensual = hotel_operations_df.groupby("Mes")["Ingresos_Hotel"].sum()

plt.figure(figsize=(10, 6))
sns.barplot(x=ingresos_hotel_mensual.index, y=ingresos_hotel_mensual.values, palette="viridis")
plt.title("Ingresos Hoteleros Mensuales (Casino Pullman, 2023)")
plt.xlabel("Mes")
plt.ylabel("Ingresos Totales (€)")
plt.grid(True)
plt.savefig("/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/visualizations/hotel_revenue_monthly.png")
plt.close()

# --- Análisis de Ingresos del Casino ---
# Ingresos Brutos por Juego
ingresos_juego = casino_revenue_df.groupby("Juego")["Ingresos_Brutos"].sum().sort_values(ascending=False)

plt.figure(figsize=(12, 7))
sns.barplot(x=ingresos_juego.index, y=ingresos_juego.values, palette="magma")
plt.title("Ingresos Brutos por Tipo de Juego (Casino Pullman, 2023)")
plt.xlabel("Tipo de Juego")
plt.ylabel("Ingresos Brutos Totales (€)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/visualizations/casino_revenue_by_game.png")
plt.close()

# Ganancia Neta Mensual del Casino
casino_revenue_df["Mes"] = casino_revenue_df["Fecha"].dt.month
ganancia_neta_mensual = casino_revenue_df.groupby("Mes")["Ganancia_Neta"].sum()

plt.figure(figsize=(10, 6))
sns.lineplot(x=ganancia_neta_mensual.index, y=ganancia_neta_mensual.values)
plt.title("Ganancia Neta Mensual del Casino (Casino Pullman, 2023)")
plt.xlabel("Mes")
plt.ylabel("Ganancia Neta Total (€)")
plt.grid(True)
plt.savefig("/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/visualizations/casino_net_profit_monthly.png")
plt.close()

# --- Análisis de Demografía de Clientes ---
# Distribución de Edades de Clientes
plt.figure(figsize=(10, 6))
sns.histplot(clientes_df["Edad"], bins=20, kde=True)
plt.title("Distribución de Edades de Clientes (Casino Pullman)")
plt.xlabel("Edad")
plt.ylabel("Frecuencia")
plt.grid(True)
plt.savefig("/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/visualizations/customer_age_distribution.png")
plt.close()

# Gasto Promedio por Ciudad de Origen
gasto_ciudad = clientes_df.groupby("Ciudad_Origen")["Gasto_Promedio_Casino"].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 7))
sns.barplot(x=gasto_ciudad.index, y=gasto_ciudad.values, palette="cividis")
plt.title("Gasto Promedio en Casino por Ciudad de Origen (Casino Pullman)")
plt.xlabel("Ciudad de Origen")
plt.ylabel("Gasto Promedio (€)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("/home/ubuntu/data-analytics-portfolio/03-casino-pullman-business-intelligence/visualizations/avg_spend_by_city.png")
plt.close()

print("Análisis y visualizaciones para Casino Pullman generados exitosamente.")


