import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ── Configuración de la página (debe ir primero) ──
st.set_page_config(
    page_title="Mi App Streamlit",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .stApp { background-color: #f7f8fc; }
    h1 { color: #185FA5; font-weight: 600; }
    .stButton>button {
        background-color: #185FA5;
        color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


# ── Contenido principal ──
st.title("🚀 Mi primera app con Streamlit")
st.subheader("Explorando los componentes básicos")
st.write("Bienvenido a tu primera aplicación de datos.")


st.markdown("---")

st.markdown("""
## 📝 Sección de Markdown

Streamlit soporta **negrita**, *cursiva*, `código inline` y:

- Listas con **formato**
- [Links](https://streamlit.io)

> Bloques de cita también funcionan
""")


st.subheader("🎛️ Widgets interactivos")

edad = st.slider("Selecciona tu edad", 1, 100, 25)
ciudad = st.selectbox("¿En qué ciudad vives?", 
    ["Bogotá", "Medellín", "Cali", "Barranquilla"])
nombre = st.text_input("Tu nombre", placeholder="Escribe aquí...")

if st.button("Calcular"):
    st.balloons()


col1, col2 = st.columns(2)
with col1:
    st.metric(label="Temperatura", value="28 °C", delta="2 °C")
with col2:
    st.metric(label="Humedad", value="65%", delta="-5%")


with st.sidebar:
    st.header("⚙️ Configuración")
    tema = st.radio("Estilo de gráficas", 
        ["whitegrid", "darkgrid", "ticks"])

with st.expander("📖 ¿Cómo usar esta app?"):
    st.write("Ajusta los parámetros en la barra lateral.")


np.random.seed(42)
df = pd.DataFrame({
    "fecha": pd.date_range("2024-01", periods=12, freq="ME"),
    "ventas": np.random.randint(100, 500, 12),
    "ciudad": np.random.choice(["Medellín", "Bogotá", "Cali"], 12)
})
st.dataframe(df, use_container_width=True)


fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df["fecha"], df["ventas"], marker="o", linewidth=2.5)
ax.set_title("Ventas mensuales 2024")
st.pyplot(fig)
plt.close(fig)


sns.set_theme(style="whitegrid")
fig, ax = plt.subplots()
sns.barplot(data=df, x="ciudad", y="ventas", ax=ax)
st.pyplot(fig)
plt.close(fig)


st.line_chart(df.set_index("fecha")["ventas"])
st.bar_chart(df.groupby("ciudad")["ventas"].sum())


csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Descargar CSV",
    data=csv_data,
    file_name="ventas_2024.csv",
    mime="text/csv"
)


