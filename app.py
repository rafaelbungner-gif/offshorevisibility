import streamlit as st
import math
import base64
from pathlib import Path

# ─────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Visibilidade Offshore",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

R = 6_367_000  # Raio médio da Terra (metros)

# ─────────────────────────────────────────────────
# HELPERS & MOTOR DO DIAGRAMA
# ─────────────────────────────────────────────────
def calc_hidden_height(c_km: float, k: float) -> float:
    """h = [c² * (1 - k)] / (2 * r)  — c em metros"""
    c_m = c_km * 1000
    return (c_m**2 * (1 - k)) / (2 * R)

def calc_dmax(h_obs: float, h_turb: float, k: float) -> float:
    """D_max = √[(2r·H_obs)/(1-k)] + √[(2r·H_turb)/(1-k)]  — resultado em km"""
    factor = 2 * R / (1 - k)
    return (math.sqrt(factor * h_obs) + math.sqrt(factor * h_turb)) / 1000

def render_dynamic_svg(h_obs, h_turb):
    """Gera o diagrama SVG em tempo real baseado nos inputs"""
    t_h_px = min(150, max(40, h_turb * 0.5))
    o_h_px = min(80, max(10, h_obs * 2))
    
    t_y = 200 - t_h_px
    o_y = 200 - o_h_px
    
    svg = f"""
    <svg viewBox="0 0 800 250" xmlns="http://www.w3.org/2000/svg" style="width: 100%; height: auto; display: block; background: #0a1628;">
        <path d="M 0 200 Q 400 170 800 200 L 800 250 L 0 250 Z" fill="#0d1e33" stroke="#4fc3f7" stroke-width="2"/>
        
        <path d="M 100 {o_y} Q 400 120 700 {t_y}" fill="transparent" stroke="#4fc3f7" stroke-dasharray="6,6" stroke-width="2"/>
        
        <rect x="95" y="{o_y}" width="10" height="{o_h_px}" fill="#d4e6f1"/>
        <circle cx="100" cy="{o_y}" r="4" fill="#4fc3f7"/>
        <text x="100" y="{o_y - 10}" fill="#d4e6f1" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">H_obs: {h_obs:.1f}m</text>
        
        <line x1="700" y1="200" x2="700" y2="{t_y}" stroke="#d4e6f1" stroke-width="4"/>
        <circle cx="700" cy="{t_y}" r="4" fill="#ffb300" stroke="#4fc3f7" stroke-width="2"/>
        <line x1="700" y1="{t_y}" x2="700" y2="{t_y - 25}" stroke="#4fc3f7" stroke-width="3"/>
        <line x1="700" y1="{t_y}" x2="680" y2="{t_y + 15}" stroke="#4fc3f7" stroke-width="3"/>
        <line x1="700" y1="{t_y}" x2="720" y2="{t_y + 15}" stroke="#4fc3f7" stroke-width="3"/>
        <text x="700" y="{t_y - 30}" fill="#d4e6f1" font-family="sans-serif" font-size="12" font-weight="bold" text-anchor="middle">H_turb: {h_turb:.0f}m</text>
    </svg>
    """
    return base64.b64encode(svg.encode('utf-8')).decode('utf-8')

# ─────────────────────────────────────────────────
# CSS ORIGINAL
# ─────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #07111f; color: #d4e6f1; }

.app-header { text-align: center; padding: 2.5rem 1rem 0.5rem; }
.app-header h1 { font-family: 'Playfair Display', serif; font-size: 2.5rem; font-weight: 700; color: #e8f4fd; margin-bottom: 0.3rem; }
.app-header p { font-size: 1rem; color: #7fb3d3; font-weight: 300; margin: 0; }
.badge-row { display: flex; justify-content: center; gap: 0.6rem; margin-top: 0.8rem; flex-wrap: wrap; }
.badge { background: rgba(79, 195, 247, 0.1); border: 1px solid rgba(79, 195, 247, 0.3); color: #4fc3f7; font-size: 0.7rem; padding: 0.25rem 0.75rem; border-radius: 999px; text-transform: uppercase; font-weight: 500; }

.diagram-wrap { border-radius: 12px; overflow: hidden; border: 1px solid rgba(79, 195, 247, 0.15); margin: 1.5rem 0; background: #0a1628; }
.diagram-wrap img { width: 100%; display: block; }

.module-card { background: #0d1e33; border: 1px solid rgba(79, 195, 247, 0.18); border-radius: 14px; padding: 1.6rem 1.8rem 1.4rem; height: 100%; }
.module-title { font-family: 'Playfair Display', serif; font-size: 1.2rem; color: #e8f4fd; margin-bottom: 0.2rem; }
.module-subtitle { font-size: 0.82rem; color: #5d9bbf; margin-bottom: 1.2rem; font-weight: 300; }

.result-box { background: linear-gradient(135deg, #0d3460 0%, #0a2545 100%); border: 1px solid rgba(79, 195, 247, 0.35); border-radius: 12px; padding: 1.2rem 1.4rem; text-align: center; margin-top: 1.2rem; }
.result-label { font-size: 0.75rem; letter-spacing: 1.8px; text-transform: uppercase; color: #7fb3d3; margin-bottom: 0.4rem; }
.result-value { font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 700; line-height: 1; color: #4fc3f7; text-shadow: 0 0 20px rgba(79,195,247,0.4); }
.result-unit { font-size: 1rem; color: #90caf9; margin-top: 0.2rem; }
.result-box-orange .result-value { color: #ffb300; text-shadow: 0 0 20px rgba(255,179,0,0.4); }
.result-box-orange { border-color: rgba(255,179,0,0.35); }

.section-divider { border: none; border-top: 1px solid rgba(79, 195, 247, 0.1); margin: 1rem 0; }

div[data-testid="stNumberInput"] input { background: #0a2545 !important; border: 1px solid rgba(79,195,247,0.3) !important; color: #d4e6f1 !important; border-radius: 8px !important; }
.stExpander { background: rgba(13, 30, 51, 0.6) !important; border: 1px solid rgba(79, 195, 247, 0.12) !important; border-radius: 10px !important; }
label { color: #90c8e0 !important; font-size: 0.88rem !important; font-weight: 400 !important; }
.stExpander summary { color: #7fb3d3 !important; font-size: 0.82rem !important; }

.app-footer { text-align: center; padding: 2rem 1rem; font-size: 0.75rem; color: #2d5573; letter-spacing: 0.5px; }
</style>
""",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────
st.markdown(
    """
<div class="app-header">
  <h1>🌊 Calculadora de Visibilidade Offshore</h1>
  <p>Parâmetros espaciais de visibilidade de aerogeradores baseados em óptica atmosférica e geodésia</p>
  <div class="badge-row">
    <span class="badge">BOEM</span>
    <span class="badge">NatureScot</span>
    <span class="badge">Geodésia Clássica</span>
    <span class="badge">r = 6.367.000 m</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# Espaço reservado para o diagrama que será atualizado no final do código
diagram_placeholder = st.empty()

st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# TWO MODULES SIDE BY SIDE
# ─────────────────────────────────────────────────
col1, gap, col2 = st.columns([1, 0.06, 1])

# ════════════════════════════════════════════════
# MÓDULO 1 — Altura Oculta
# ════════════════════════════════════════════════
with col1:
    st.markdown(
        """
<div class="module-card">
  <div class="module-title">Módulo 1 · Altura Oculta</div>
  <div class="module-subtitle">Metros da base do aerogerador ocultos pela curvatura e refração</div>
</div>
""",
        unsafe_allow_html=True,
    )
    
    # Nova apresentação elegante da fórmula
    st.latex(r"h = \frac{c^2 \cdot (1 - k)}{2 \cdot r}")
    st.markdown("<div style='text-align:center; color:#5d9bbf; font-size:0.78rem; margin-bottom: 1.4rem;'>c em metros · r = 6.367.000 m</div>", unsafe_allow_html=True)

    c_km = st.number_input(
        "Distância da costa (km)",
        min_value=1.0,
        max_value=200.0,
        value=20.0,
        step=1.0,
        format="%.1f",
        key="c_km",
    )

    with st.expander("⚙️ Parâmetros Avançados"):
        k1 = st.number_input(
            "Coeficiente de refração (k)",
            min_value=0.0,
            max_value=0.25,
            value=0.075,
            step=0.005,
            format="%.3f",
            key="k1",
            help="Padrão BOEM/NatureScot: 0,075. Varia com temperatura e umidade do ar.",
        )

    h_result = calc_hidden_height(c_km, k1)

    st.markdown(
        f"""
<div class="result-box result-box-orange">
  <div class="result-label">Altura Oculta (h)</div>
  <div class="result-value">{h_result:.1f}</div>
  <div class="result-unit">metros</div>
</div>
""",
        unsafe_allow_html=True,
    )

    if h_result >= 1:
        st.caption(f"💡 A {c_km:.1f} km da costa, os primeiros **{h_result:.1f} m** da estrutura ficam abaixo do horizonte visual.")
    else:
        st.caption(f"💡 A {c_km:.1f} km da costa, apenas **{h_result*100:.0f} cm** da base ficam ocultos — estrutura visível.")

# ════════════════════════════════════════════════
# MÓDULO 2 — Distância Máxima de Visibilidade
# ════════════════════════════════════════════════
with col2:
    st.markdown(
        """
<div class="module-card">
  <div class="module-title">Módulo 2 · Distância Máxima</div>
  <div class="module-subtitle">Raio teórico máximo até onde a ponta da pá é visível</div>
</div>
""",
        unsafe_allow_html=True,
    )
    
    # Nova apresentação elegante da fórmula
    st.latex(r"D_{max} = \sqrt{\frac{2 \cdot r \cdot H_{obs}}{1 - k}} + \sqrt{\frac{2 \cdot r \cdot H_{turb}}{1 - k}}")
    st.markdown("<div style='text-align:center; color:#5d9bbf; font-size:0.78rem; margin-bottom: 1.4rem;'>resultado em km · r = 6.367.000 m</div>", unsafe_allow_html=True)

    h_obs = st.number_input(
        "Altura do observador na costa (m)",
        min_value=0.5,
        max_value=200.0,
        value=1.7,
        step=0.5,
        format="%.1f",
        key="h_obs",
    )

    h_turb = st.number_input(
        "Altura total do aerogerador (m)",
        min_value=50.0,
        max_value=500.0,
        value=200.0,
        step=5.0,
        format="%.0f",
        key="h_turb",
    )

    with st.expander("⚙️ Parâmetros Avançados"):
        k2 = st.number_input(
            "Coeficiente de refração (k)",
            min_value=0.0,
            max_value=0.25,
            value=0.130,
            step=0.005,
            format="%.3f",
            key="k2",
            help="Padrão NatureScot para D_max: 0,13. Reflete condições típicas no mar aberto.",
        )

    d_result = calc_dmax(h_obs, h_turb, k2)

    st.markdown(
        f"""
<div class="result-box">
  <div class="result-label">Distância Máxima (D_max)</div>
  <div class="result-value">{d_result:.1f}</div>
  <div class="result-unit">quilômetros</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.caption(f"💡 Observador a **{h_obs:.1f} m** de altura enxerga a ponta da pá de **{h_turb:.0f} m** até **{d_result:.1f} km** de distância.")

# ─────────────────────────────────────────────────
# RENDERIZAR O DIAGRAMA DINÂMICO NO TOPO
# ─────────────────────────────────────────────────
b64_svg = render_dynamic_svg(h_obs, h_turb)
diagram_placeholder.markdown(
    f'<div class="diagram-wrap"><img src="data:image/svg+xml;base64,{b64_svg}" alt="Diagrama de visibilidade dinâmico"/></div>',
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────
st.markdown("<hr class='section-divider'/>", unsafe_allow_html=True)
st.markdown(
    """
<div class="app-footer">
  Baseado nas diretrizes <strong>BOEM</strong> (Bureau of Ocean Energy Management) e <strong>NatureScot</strong> · 
  Fórmulas de geodésia clássica e óptica atmosférica · Raio da Terra: 6.367.000 m
</div>
""",
    unsafe_allow_html=True,
)
