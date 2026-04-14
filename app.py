import streamlit as st
import math

# ─────────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Visibilidade Offshore",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

R = 6_367_000  # Raio médio da Terra (metros)

# ─────────────────────────────────────────────────
# FUNÇÕES DE CÁLCULO
# ─────────────────────────────────────────────────
def calc_hidden_height(c_km, k):
    """Calcula a altura oculta pela curvatura."""
    c_m = c_km * 1000
    return (c_m**2 * (1 - k)) / (2 * R)

def calc_dmax(h_obs, h_turb, k):
    """Calcula a distância teórica máxima."""
    factor = 2 * R / (1 - k)
    return (math.sqrt(factor * h_obs) + math.sqrt(factor * h_turb)) / 1000

# ─────────────────────────────────────────────────
# MOTOR DO DIAGRAMA DINÂMICO
# ─────────────────────────────────────────────────
def render_dynamic_svg(h_obs, h_turb, d_max):
    """Gera um SVG em tempo real que altera a proporção do desenho conforme os dados."""
    
    # Cálculos de escala para animar o desenho na tela
    # A turbina varia visualmente entre um tamanho mínimo e máximo
    t_height = max(40, min(180, (h_turb / 350) * 150))
    t_top = 250 - t_height
    
    # O observador também varia visualmente
    o_height = max(10, min(100, (h_obs / 100) * 60))
    o_top = 250 - o_height

    svg = f"""
    <svg viewBox="0 0 800 320" xmlns="http://www.w3.org/2000/svg" style="background-color: #07111f; border-radius: 10px; border: 1px solid #1e3a5f; width: 100%;">
        <path d="M 0 250 Q 400 200 800 250 L 800 320 L 0 320 Z" fill="#0d1e33" stroke="#4fc3f7" stroke-width="2"/>
        
        <path d="M 50 {o_top} Q 400 150 750 {t_top}" fill="transparent" stroke="#4fc3f7" stroke-dasharray="6,6" stroke-width="2"/>
        
        <rect x="45" y="{o_top}" width="10" height="{o_height}" fill="#d4e6f1"/>
        <circle cx="50" cy="{o_top}" r="5" fill="#4fc3f7"/>
        <text x="10" y="{o_top - 15}" fill="#d4e6f1" font-family="sans-serif" font-size="14" font-weight="bold">H_obs: {h_obs}m</text>
        
        <line x1="750" y1="250" x2="750" y2="{t_top}" stroke="#d4e6f1" stroke-width="6"/>
        <circle cx="750" cy="{t_top}" r="5" fill="#07111f" stroke="#4fc3f7" stroke-width="2"/>
        <line x1="750" y1="{t_top}" x2="750" y2="{t_top - 35}" stroke="#4fc3f7" stroke-width="4"/>
        <line x1="750" y1="{t_top}" x2="720" y2="{t_top + 20}" stroke="#4fc3f7" stroke-width="4"/>
        <line x1="750" y1="{t_top}" x2="780" y2="{t_top + 20}" stroke="#4fc3f7" stroke-width="4"/>
        <text x="650" y="{t_top - 20}" fill="#d4e6f1" font-family="sans-serif" font-size="14" font-weight="bold">H_turb: {h_turb}m</text>
        
        <rect x="300" y="80" width="200" height="40" rx="5" fill="#0d1e33" stroke="#4fc3f7" stroke-width="1"/>
        <text x="400" y="106" fill="#4fc3f7" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">D_max = {d_max:.1f} km</text>
    </svg>
    """
    return svg


# ─────────────────────────────────────────────────
# INTERFACE DO USUÁRIO
# ─────────────────────────────────────────────────
st.title("🌊 Calculadora de Visibilidade Offshore")
st.markdown("---")

# ======== MÓDULO 1 ========
st.header("Módulo 1: Correção de Altura Oculta ($h$)")
st.markdown("Fórmula utilizada para compensação da curvatura:")
st.latex(r"h = \frac{c^2 \cdot (1 - k)}{2 \cdot R}")

st.markdown("<br>", unsafe_allow_html=True) # Espaçamento confortável

col1, col2 = st.columns(2)
with col1:
    c_km = st.number_input("Distância do parque eólico até a costa (km):", min_value=1.0, max_value=200.0, value=30.0, step=1.0)
with col2:
    k1 = st.number_input("Coeficiente de Refração Atmosférica (k):", min_value=0.0, max_value=0.3, value=0.075, step=0.005, format="%.3f")

h_hidden = calc_hidden_height(c_km, k1)

st.info(f"**Resultado:** A uma distância de {c_km} km, cerca de **{h_hidden:.1f} metros** da base da estrutura estarão invisíveis devido à curvatura da Terra.")

st.markdown("---")

# ======== MÓDULO 2 ========
st.header("Módulo 2: Distância Máxima de Visibilidade ($D_{max}$)")
st.markdown("Fórmula utilizada para limite visual geométrico:")
st.latex(r"D_{max} = \sqrt{\frac{2 \cdot R \cdot H_{obs}}{1 - k}} + \sqrt{\frac{2 \cdot R \cdot H_{turb}}{1 - k}}")

st.markdown("<br>", unsafe_allow_html=True) # Espaçamento confortável

col3, col4, col5 = st.columns(3)
with col3:
    h_obs = st.number_input("Altura do Observador (H_obs em metros):", min_value=0.0, max_value=500.0, value=2.0, step=1.0)
with col4:
    h_turb = st.number_input("Altura da Turbina (H_turb em metros):", min_value=50.0, max_value=500.0, value=260.0, step=10.0)
with col5:
    k2 = st.number_input("Refração Atmosférica (k) - Padrão BOEM:", min_value=0.0, max_value=0.3, value=0.130, step=0.005, format="%.3f")

d_max = calc_dmax(h_obs, h_turb, k2)

# Renderiza o diagrama dinâmico gerado pelo Python!
st.markdown("### Diagrama Visual Interativo")
st.components.v1.html(render_dynamic_svg(h_obs, h_turb, d_max), height=350)
