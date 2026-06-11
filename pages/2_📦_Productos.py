import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Productos", page_icon="📦", layout="wide")
st.title("📦 Catálogo de Productos")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📋 Catálogo", use_container_width=True):
        st.session_state.menu = "catalogo"
with col2:
    if st.button("➕ Nuevo Producto", use_container_width=True):
        st.session_state.menu = "nuevo"
with col3:
    if st.button("📊 Estadísticas", use_container_width=True):
        st.session_state.menu = "estadisticas"

st.divider()

@st.cache_data
def cargar_productos():
    return pd.DataFrame({
        "ID": [1, 2, 3, 4, 5, 6, 7],
        "Nombre": ["Laptop Lenovo IdeaPad", "Mouse Logitech MX", "Switch TP-Link 8p",
                   "Teclado Mecánico Redragon", "Webcam Full HD Logitech",
                   "Monitor LG 24\"", "Router WiFi 6 Asus"],
        "Categoría": ["Electrónica", "Periféricos", "Redes", "Periféricos",
                      "Accesorios", "Electrónica", "Redes"],
        "Precio": [850, 75, 120, 95, 65, 310, 145],
        "Stock": [12, 40, 25, 30, 18, 8, 15]
    })

df = cargar_productos()

st.image("https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=800&h=200&fit=crop",
         caption="Catálogo de Productos", use_container_width=True)

menu_actual = st.session_state.get("menu", "catalogo")

if menu_actual == "catalogo":
    st.subheader("📋 Listado de Productos")

    categoria_filter = st.multiselect("Filtrar por categoría", options=df["Categoría"].unique())

    df_filtrado = df.copy()
    if categoria_filter:
        df_filtrado = df_filtrado[df_filtrado["Categoría"].isin(categoria_filter)]

    st.dataframe(df_filtrado, use_container_width=True)
    st.caption(f"Mostrando {len(df_filtrado)} de {len(df)} productos")

elif menu_actual == "nuevo":
    st.subheader("➕ Registrar Nuevo Producto")
    with st.form("form_producto"):
        nombre = st.text_input("Nombre del producto")
        categoria = st.selectbox("Categoría", ["Electrónica", "Periféricos", "Redes", "Accesorios"])
        precio = st.number_input("Precio (USD)", min_value=0)
        stock = st.number_input("Stock inicial", min_value=0)
        enviado = st.form_submit_button("Guardar Producto")
        if enviado:
            st.success(f"✅ Producto '{nombre}' registrado correctamente")

elif menu_actual == "estadisticas":
    st.subheader("📊 Estadísticas de Productos")

    fig, ax = plt.subplots(figsize=(8, 5))
    colores = ["steelblue" if c == "Electrónica" else
               "darkorange" if c == "Periféricos" else
               "mediumseagreen" if c == "Redes" else "orchid"
               for c in df["Categoría"]]
    bars = ax.bar(df["Nombre"], df["Precio"], color=colores)
    ax.set_title("Precio por Producto", fontsize=14)
    ax.set_ylabel("Precio (USD)")
    ax.set_xticklabels(df["Nombre"], rotation=30, ha="right", fontsize=9)
    for bar, precio in zip(bars, df["Precio"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                f"${precio:,}", ha="center", fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.metric("Total de Productos", len(df))