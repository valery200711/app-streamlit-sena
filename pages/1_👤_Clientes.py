import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Clientes", page_icon="👤", layout="wide")

st.title("👤 Gestión de Clientes")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📋 Listado", use_container_width=True):
        st.session_state.menu = "listado"
with col2:
    if st.button("➕ Nuevo Cliente", use_container_width=True):
        st.session_state.menu = "nuevo"
with col3:
    if st.button("📊 Estadísticas", use_container_width=True):
        st.session_state.menu = "estadisticas"

st.divider()

@st.cache_data
def cargar_clientes():
    return pd.DataFrame({
        "ID": [1, 2, 3, 4, 5],
        "Nombre": ["Ana García", "Luis Pérez", "María Torres", "Carlos Ruiz", "Sofía Mendoza"],
        "Ciudad": ["Medellín", "Bogotá", "Cali", "Barranquilla", "Medellín"],
        "Ventas": [12500, 8700, 15400, 6200, 14300],
        "Antigüedad_meses": [24, 15, 36, 8, 42]
    })

df = cargar_clientes()

st.image("https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&h=200&fit=crop", 
         caption="Panel de Clientes", use_container_width=True)

menu_actual = st.session_state.get("menu", "listado")

if menu_actual == "listado":
    st.subheader("📋 Listado de Clientes")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        ciudad_filter = st.multiselect("Filtrar por ciudad", options=df["Ciudad"].unique())
    with col_f2:
        ventas_min = st.slider("Ventas mínimas", 0, int(df["Ventas"].max()), 0)
    
    df_filtrado = df.copy()
    if ciudad_filter:
        df_filtrado = df_filtrado[df_filtrado["Ciudad"].isin(ciudad_filter)]
    if ventas_min > 0:
        df_filtrado = df_filtrado[df_filtrado["Ventas"] >= ventas_min]
    
    st.dataframe(df_filtrado, use_container_width=True)
    st.caption(f"Mostrando {len(df_filtrado)} de {len(df)} clientes")

elif menu_actual == "nuevo":
    st.subheader("➕ Registrar Nuevo Cliente")
    with st.form("form_cliente"):
        nombre = st.text_input("Nombre completo")
        ciudad = st.selectbox("Ciudad", ["Medellín", "Bogotá", "Cali", "Barranquilla"])
        ventas = st.number_input("Ventas iniciales", min_value=0)
        enviado = st.form_submit_button("Guardar Cliente")
        if enviado:
            st.success(f"✅ Cliente {nombre} registrado correctamente")

elif menu_actual == "estadisticas":
    st.subheader("📊 Estadísticas de Clientes")
    
    tipo_grafico = st.radio("Selecciona gráfico:", 
        ["Ventas por Ciudad", "Antigüedad vs Ventas"], horizontal=True)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    if tipo_grafico == "Ventas por Ciudad":
        ventas_ciudad = df.groupby("Ciudad")["Ventas"].sum()
        ventas_ciudad.plot(kind="bar", color="steelblue", ax=ax)
        ax.set_title("Total de Ventas por Ciudad", fontsize=14)
        ax.set_ylabel("Ventas (USD)")
        for i, v in enumerate(ventas_ciudad):
            ax.text(i, v + 200, f"${v:,.0f}", ha="center", fontsize=10)
    else:
        ax.scatter(df["Antigüedad_meses"], df["Ventas"], s=100, alpha=0.7, color="darkorange")
        ax.set_title("Relación: Antigüedad vs Ventas", fontsize=14)
        ax.set_xlabel("Antigüedad (meses)")
        ax.set_ylabel("Ventas (USD)")
        z = np.polyfit(df["Antigüedad_meses"], df["Ventas"], 1)
        p = np.poly1d(z)
        ax.plot(df["Antigüedad_meses"], p(df["Antigüedad_meses"]), "r--", label="Tendencia")
        ax.legend()
    
    st.pyplot(fig)
    plt.close(fig)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        st.metric("Total Clientes", len(df))
    with col_m2:
        st.metric("Ventas Totales", f"${df['Ventas'].sum():,.0f}")
    with col_m3:
        st.metric("Ticket Promedio", f"${df['Ventas'].mean():,.0f}")