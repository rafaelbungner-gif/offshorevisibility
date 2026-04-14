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
# FUNÇÕES MATEMÁTICAS
# ─────────────────────────────────────────────────
def calc_hidden_height(c_km: float, k: float) -> float:
    """Calcula a altura oculta pela curvatura da Terra."""
    c_m = c_km * 1000
    return (c_m**2 * (1 - k)) / (2 * R)

def calc_dmax(h_obs: float, h_turb: float, k: float) -> float:
    """Calcula a distância teórica máxima geométrica (D_max)."""
    factor = 2 * R / (1 - k)
    return (math.sqrt(factor * h_obs) + math.sqrt(factor * h_turb)) / 1000

# ─────────────────────────────────────────────────
# MOTOR DO DIAGRAMA DINÂMICO
# ─────────────────────────────────────────────────
def render_dynamic_svg(h_obs, h_turb, d_max):
    """Gera um gráfico vetorial em tempo real baseado nos inputs."""
    
    # Cálculos de proporção para animação na tela (Limites visuais)
    t_h_px = min(180, max(50, h_turb * 0.6))
    o_h_px = min(100, max(15, h_obs * 2))
    
    t_y = 250 - t_h_px
    o_y = 250 - o_h_px

    svg = f"""
    <svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg" style="background-color: #07111f; border-radius: 10px; border: 1px solid #1e3a5f; width: 100%; margin-bottom: 20px;">
        <path d="M 0 250 Q 400 210 800 250 L 800 300 L 0 300 Z" fill="#0d1e33" stroke="#4fc3f7" stroke-width="2"/>
        
        <path d="M 100 {o_y} Q 400 150 700 {t_y}" fill="transparent" stroke="#4fc3f7" stroke-dasharray="6,6" stroke-width="2"/>
        
        <rect x="95" y="{o_y}" width="10" height="{o_h_px}" fill="#d4e6f1"/>
        <circle cx="100" cy="{o_y}" r="4" fill="#4fc3f7"/>
        <text x="100" y="{o_y - 12}" fill="#d4e6f1" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">H_obs: {h_obs:.0f}m</text>
        
        <line x1="700" y1="250" x2="700" y2="{t_y}" stroke="#d4e6f1" stroke-width="5"/>
        <circle cx="700" cy="{t_y}" r="4" fill="#07111f" stroke="#4fc3f7" stroke-width="2"/>
        <line x1="700" y1="{t_y}" x2="700" y2="{t_y - 30}" stroke="#4fc3f7" stroke-width="3"/>
        <line x1="700" y1="{t_y}" x2="675" y2="{t_y + 15}" stroke="#4fc3f7" stroke-width="3"/>
        <line x1="700" y1="{t_y}" x2="725" y2="{t_y + 15}" stroke="#4fc3f7" stroke-width="3"/>
        <text x="700" y="{t_y - 40}" fill="#d4e6f1" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">H_turb: {h_turb:.0f}m</text>
        
        <rect x="300" y="40" width="200" height="40" rx="5" fill="#0d1e33" stroke="#4fc3f7" stroke-width="1"/>
        <text x="400" y="66" fill="#4fc3f7" font-family="sans-serif" font-size="18" font-weight="bold" text-anchor="middle">D_max = {d_max:.1f} km</text>
    </svg>
    """
    return svg

# ─────────────────────────────────────────────────
# INTERFACE DO USUÁRIO
# ─────────────────────────────────────────────────
st.title("🌊 Calculadora de Visibilidade Offshore")
st.markdown("Ferramenta para análise espacial baseada em óptica atmosférica e geodésia.")
st.markdown("---")

# ======== MÓDULO 1: ALTURA OCULTA ========
st.header("Módulo 1: Correção de Altura Oculta ($h$)")
st.markdown("Fórmula utilizada para cálculo de perda visual:")
# Fórmula em tipografia matemática (LaTeX)
st.latex(r"h = \frac{c^2 \cdot (1 - k)}{2 \cdot R}")
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    c_km = st.number_input("Distância até a costa (km):", min_value=1.0, max_value=200.0, value=30.0, step=1.0)
with col2:
    k1 = st.number_input("Coeficiente de Refração (k):", min_value=0.0, max_value=0.3, value=0.075, step=0.005, format="%.3f")

h_hidden = calc_hidden_height(c_km, k1)
st.info(f"**Resultado:** A uma distância de {c_km} km, cerca de **{h_hidden:.1f} metros** da base da estrutura estarão invisíveis devido à curvatura da Terra.")

st.markdown("---")

# ======== MÓDULO 2: DISTÂNCIA MÁXIMA ========
st.header("Módulo 2: Distância Máxima de Visibilidade ($D_{max}$)")
st.markdown("Fórmula geométrica do limite do horizonte visual:")
# Fórmula em tipografia matemática (LaTeX)
st.latex(r"D_{max} = \sqrt{\frac{2 \cdot R \cdot H_{obs}}{1 - k}} + \sqrt{\frac{2 \cdot R \cdot H_{turb}}{1 - k}}")
st.markdown("<br>", unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)
with col3:
    h_obs = st.number_input("Altura do Observador (m):", min_value=1.0, max_value=500.0, value=2.0, step=1.0)
with col4:
    h_turb = st.number_input("Altura da Turbina (m):", min_value=50.0, max_value=500.0, value=260.0, step=5.0)
with col5:
    k2 = st.number_input("Refração (k) - Padrão BOEM:", min_value=0.0, max_value=0.3, value=0.130, step=0.005, format="%.3f")

d_max = calc_dmax(h_obs, h_turb, k2)

# Renderização do Diagrama Dinâmico!
st.markdown("### Diagrama Visual Interativo")
st.components.v1.html(render_dynamic_svg(h_obs, h_turb, d_max), height=320)

# Renderiza o diagrama dinâmico gerado pelo Python!
st.markdown("### Diagrama Visual Interativo")
st.components.v1.html(render_dynamic_svg(h_obs, h_turb, d_max), height=350)
