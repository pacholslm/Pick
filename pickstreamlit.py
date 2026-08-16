import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import math

st.set_page_config(page_title="Teorema de Pick", page_icon="📐", layout="centered")

st.title("Teorema de Pick: Frontera e Interior")
st.write("Calcula el área de un polígono en una cuadrícula utilizando la fórmula de Pick.")

# Selección del número de vértices
n = st.number_input("Número de vértices del polígono (mínimo 3):", min_value=3, max_value=20, value=4, step=1)

st.markdown("### Coordenadas de los Vértices")
st.markdown("Introduce las coordenadas enteras para cada vértice:")

vx = []
vy = []

# Crear campos de entrada organizados en dos columnas (X e Y) por cada vértice
for i in range(int(n)):
    col1, col2 = st.columns(2)
    with col1:
        x = st.number_input(f"Vértice {i+1} - X", value=i, step=1, format="%d", key=f"vx_{i}")
        vx.append(int(x))
    with col2:
        # Valores predeterminados sencillos para evitar polígonos inválidos iniciales
        default_y = 0 if i % 2 == 0 else 2
        y = st.number_input(f"Vértice {i+1} - Y", value=default_y, step=1, format="%d", key=f"vy_{i}")
        vy.append(int(y))

st.markdown("---")

if st.button("Analizar Teorema de Pick", type="primary"):
    try:
        vertices = list(zip(vx, vy))
        path = mpath.Path(vertices + [vertices[0]])

        # 1. Calcular Puntos en la Frontera (B)
        puntos_b_x, puntos_b_y = [], []
        B = 0
        num_v = len(vx)
        for i in range(num_v):
            x1, y1 = vx[i], vy[i]
            x2, y2 = vx[(i + 1) % num_v], vy[(i + 1) % num_v]
            g = math.gcd(abs(x2 - x1), abs(y2 - y1))
            for j in range(g):
                puntos_b_x.append(x1 + j * (x2 - x1) // g)
                puntos_b_y.append(y1 + j * (y2 - y1) // g)
            B += g

        # 2. Calcular Puntos en el Interior (I)
        lista_frontera = list(zip(puntos_b_x, puntos_b_y))
        
        min_x, max_x = min(vx), max(vx)
        min_y, max_y = min(vy), max(vy)
        
        puntos_i_x, puntos_i_y = [], []
        for ix in range(min_x, max_x + 1):
            for iy in range(min_y, max_y + 1):
                if path.contains_point((ix, iy)) and (ix, iy) not in lista_frontera:
                    puntos_i_x.append(ix)
                    puntos_i_y.append(iy)
        
        I = len(puntos_i_x)
        area = I + (B / 2) - 1

        # Mostrar métricas de resultados
        st.success("¡Análisis realizado con éxito!")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Puntos en la Frontera (B)", B)
        m2.metric("Puntos en el Interior (I)", I)
        m3.metric("Área Total", f"{area}")

        # 3. Graficar con Matplotlib
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.fill(vx + [vx[0]], vy + [vy[0]], alpha=0.1, color='gray')
        ax.plot(vx + [vx[0]], vy + [vx[0]], 'k-', lw=1)
        
        ax.scatter(puntos_b_x, puntos_b_y, color='blue', s=50, label=f'Frontera (B={B})', zorder=3)
        ax.scatter(puntos_i_x, puntos_i_y, color='red', s=50, label=f'Interior (I={I})', zorder=3)
        
        ax.set_title(f"Área = {I} + {B}/2 - 1 = {area}")
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()
        
        # Renderizar gráfico en Streamlit
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Ocurrió un error al calcular el polígono: {str(e)}")