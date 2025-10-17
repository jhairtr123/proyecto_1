import streamlit as st
import pandas as pd
import plotly.express as px

# Leer y limpiar datos
car_data = pd.read_csv('vehicles_us.csv')
car_data.dropna(subset=["model_year", "type", "price", "odometer"], inplace=True)
car_data.columns = car_data.columns.str.strip()

# Encabezado
st.header("Cuadro de mandos de vehículos en venta")

# Filtros en la barra lateral
st.sidebar.header("Filtros")

years = sorted(car_data["model_year"].unique())
selected_years = st.sidebar.multiselect("Selecciona año(s) del modelo:", years, default=years)

types = sorted(car_data["type"].unique())
selected_types = st.sidebar.multiselect("Selecciona tipo(s):", types, default=types)

min_price = int(car_data["price"].min())
max_price = int(car_data["price"].max())
price_range = st.sidebar.slider("Rango de precio:", min_price, max_price, (min_price, max_price))

# Aplicar filtros
filtered_data = car_data[
    (car_data["model_year"].isin(selected_years)) &
    (car_data["type"].isin(selected_types)) &
    (car_data["price"] >= price_range[0]) &
    (car_data["price"] <= price_range[1])
]

# Botón para descargar datos filtrados
st.download_button("Descargar datos filtrados", filtered_data.to_csv(index=False),
                   "datos_filtrados.csv", "text/csv")

# Conteo por tipo
type_counts = filtered_data["type"].value_counts().reset_index()
type_counts.columns = ["type", "count"]

# Pestañas para cada gráfico
tabs = st.tabs(["Histograma", "Dispersión", "Barras", "Caja", "Violín", "Pastel"])

with tabs[0]:
    st.subheader("Distribución del odómetro")
    fig = px.histogram(filtered_data, x="odometer", title="Distribución del odómetro")
    st.plotly_chart(fig, use_container_width=True, key="histograma")

with tabs[1]:
    st.subheader("Precio vs Odómetro")
    fig = px.scatter(filtered_data, x="odometer", y="price", color="type",
                     hover_data=["model", "model_year"], title="Precio vs Odómetro")
    st.plotly_chart(fig, use_container_width=True, key="dispersión")

with tabs[2]:
    st.subheader("Cantidad de vehículos por tipo")
    fig = px.bar(type_counts, x="type", y="count", title="Cantidad de vehículos por tipo", color="type")
    st.plotly_chart(fig, use_container_width=True, key="barras")

with tabs[3]:
    st.subheader("Distribución de precios por tipo")
    fig = px.box(filtered_data, x="type", y="price", title="Distribución de precios por tipo")
    st.plotly_chart(fig, use_container_width=True, key="caja")

with tabs[4]:
    st.subheader("Distribución de precios (violín)")
    fig = px.violin(filtered_data, x="type", y="price", box=True, points="all",
                    title="Distribución de precios (violín)")
    st.plotly_chart(fig, use_container_width=True, key="violín")

with tabs[5]:
    st.subheader("Proporción de vehículos por tipo")
    fig = px.pie(type_counts, names="type", values="count", title="Proporción de vehículos por tipo")
    st.plotly_chart(fig, use_container_width=True, key="pastel")
