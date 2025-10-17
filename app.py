import streamlit as st
import pandas as pd
import plotly.express as px

# Leer el conjunto de datos
car_data = pd.read_csv('vehicles_us.csv')
car_data.dropna(subset=["model_year", "type", "price", "odometer"], inplace=True)
car_data.columns = car_data.columns.str.strip()


# Encabezado
st.header("Cuadro de mandos de vehículos en venta")

st.subheader("Visualizaciones rápidas")

col1, col2 = st.columns(2)

with col1:
    if st.button("Histograma rápido"):
        fig = px.histogram(car_data, x="odometer", title="Distribución del odómetro")
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if st.button("Dispersión rápida"):
        fig = px.scatter(car_data, x="odometer", y="price", color="transmission",
                         title="Precio vs Odómetro")
        st.plotly_chart(fig, use_container_width=True)


# Título
st.title("Visualización interactiva de vehículos")

# Filtros interactivos
st.sidebar.header("Filtros")

# Filtro por año del modelo
years = sorted(car_data["model_year"].dropna().unique())
selected_years = st.sidebar.multiselect("Selecciona año(s) del modelo:", years, default=years)

# Filtro por tipo de vehículo
types = sorted(car_data["type"].dropna().unique())
selected_types = st.sidebar.multiselect("Selecciona tipo(s):", types, default=types)

# Filtro por rango de precio
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

st.download_button("Descargar datos filtrados", filtered_data.to_csv(index=False),
                   "datos_filtrados.csv", "text/csv")


# Botón adicional para mostrar gráfico por tipo de vehículo
if st.button("Mostrar gráfica por tipo de vehículo"):
    st.write("Comparación de categorías por tipo de vehículo")
    type_counts = filtered_data["type"].value_counts().reset_index()
    type_counts.columns = ["type", "count"]
    fig = px.bar(type_counts, x="type", y="count", title="Cantidad de vehículos por tipo",
                 color="type")
    st.plotly_chart(fig, use_container_width=True, key="grafico_tipo_vehiculo")


type_counts = filtered_data["type"].value_counts().reset_index()
type_counts.columns = ["type", "count"]


# Selector de gráfico
chart_type = st.radio(
    "Selecciona el tipo de gráfico:",
    ("Histograma", "Dispersión", "Barras", "Caja", "Violín", "Pastel")
)

# Mostrar gráfico según selección
if chart_type == "Histograma":
    fig = px.histogram(filtered_data, x="odometer", title="Distribución del odómetro")
    st.plotly_chart(fig)

elif chart_type == "Dispersión":
    fig = px.scatter(filtered_data, x="odometer", y="price", color="type",
                     hover_data=["model", "model_year"], title="Precio vs Odómetro")
    st.plotly_chart(fig)

elif chart_type == "Barras":
    type_counts = filtered_data["type"].value_counts().reset_index()
    type_counts.columns = ["type", "count"]
    fig = px.bar(type_counts, x="type", y="count", title="Cantidad de vehículos por tipo",
                 color_discrete_sequence=["orange"])
    st.plotly_chart(fig)

elif chart_type == "Caja":
    fig = px.box(filtered_data, x="type", y="price", title="Distribución de precios por tipo")
    st.plotly_chart(fig)

elif chart_type == "Violín":
    fig = px.violin(filtered_data, x="type", y="price", box=True, points="all",
                    title="Distribución de precios (violín)")
    st.plotly_chart(fig)

elif chart_type == "Pastel":
    type_counts = filtered_data["type"].value_counts().reset_index()
    type_counts.columns = ["type", "count"]
    fig = px.pie(type_counts, names="type", values="count", title="Proporción de vehículos por tipo")
    st.plotly_chart(fig)
