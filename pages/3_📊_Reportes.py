import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import datetime

st.set_page_config(page_title="Reportes", page_icon="📊", layout="wide")
st.title("📊 Dashboards y Reportes")

st.divider()

# ── KPIs ──────────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💰 Ventas Totales", "$124,800", delta="+8.3%")
with col2:
    st.metric("👥 Clientes Activos", "57", delta="+5")
with col3:
    st.metric("📦 Productos Vendidos", "342", delta="-12")

st.divider()

# ── Datos de ejemplo ──────────────────────────────────────────────────────────
@st.cache_data
def cargar_ventas():
    return pd.DataFrame({
        "Mes": ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
        "Ventas": [8500, 9200, 7800, 10500, 11200, 9800,
                   12400, 11800, 13100, 10900, 12700, 14300],
        "Fecha": pd.date_range(start="2024-01-01", periods=12, freq="MS")
    })

df_ventas = cargar_ventas()

# ── Selector de rango de fechas ───────────────────────────────────────────────
st.subheader("📅 Filtrar por rango de fechas")

col_f1, col_f2 = st.columns(2)
with col_f1:
    fecha_inicio = st.date_input("Fecha inicio",
                                  value=datetime.date(2024, 1, 1),
                                  min_value=datetime.date(2024, 1, 1),
                                  max_value=datetime.date(2024, 12, 1))
with col_f2:
    fecha_fin = st.date_input("Fecha fin",
                               value=datetime.date(2024, 12, 1),
                               min_value=datetime.date(2024, 1, 1),
                               max_value=datetime.date(2024, 12, 1))

df_filtrado = df_ventas[
    (df_ventas["Fecha"] >= pd.Timestamp(fecha_inicio)) &
    (df_ventas["Fecha"] <= pd.Timestamp(fecha_fin))
]

# ── Gráfico de líneas ─────────────────────────────────────────────────────────
st.subheader("📈 Ventas Mensuales")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(df_filtrado["Mes"], df_filtrado["Ventas"],
        marker="o", color="steelblue", linewidth=2.5, markersize=7)
ax.fill_between(df_filtrado["Mes"], df_filtrado["Ventas"],
                alpha=0.1, color="steelblue")
ax.set_title("Evolución de Ventas por Mes", fontsize=14)
ax.set_ylabel("Ventas (USD)")
ax.set_xlabel("Mes")
for i, (mes, venta) in enumerate(zip(df_filtrado["Mes"], df_filtrado["Ventas"])):
    ax.text(i, venta + 150, f"${venta:,}", ha="center", fontsize=8.5)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.caption(f"Mostrando {len(df_filtrado)} meses — "
           f"Total período: ${df_filtrado['Ventas'].sum():,.0f} USD")

st.divider()

# ── Descarga de reporte ───────────────────────────────────────────────────────
st.subheader("⬇️ Descargar Reporte")

csv_buffer = StringIO()
df_filtrado[["Mes", "Ventas"]].to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

st.download_button(
    label="📥 Descargar reporte CSV",
    data=csv_data,
    file_name="reporte_ventas.csv",
    mime="text/csv",
    use_container_width=True
)