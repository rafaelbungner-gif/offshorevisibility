# 🌊 Calculadora de Visibilidade Offshore

Ferramenta interativa para calcular parâmetros espaciais de visibilidade de aerogeradores offshore, baseada em óptica atmosférica e geodésia (diretrizes BOEM e NatureScot).

## Estrutura do Projeto

```
offshore-visibility/
├── app.py                    # Aplicação principal Streamlit
├── requirements.txt          # Dependências Python
├── .streamlit/
│   └── config.toml           # Tema e configurações do Streamlit
└── assets/
    └── diagram.svg           # Diagrama físico do problema
```

## Como Rodar Localmente

```bash
# 1. Clone ou descompacte o projeto
cd offshore-visibility

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute
streamlit run app.py
```

Acesse em: **http://localhost:8501**

## Deploy no Streamlit Community Cloud

1. Suba o projeto para um repositório GitHub (público ou privado)
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o repositório e aponte o arquivo principal como `app.py`
4. Clique em **Deploy** — o `requirements.txt` será instalado automaticamente

## Módulos de Cálculo

### Módulo 1 — Altura Oculta (h)
```
h = [ c² × (1 − k) ] / (2 × r)
```
- `c` = distância da costa (km → convertido para metros)
- `k` = coeficiente de refração (padrão: 0,075)
- `r` = 6.367.000 m

### Módulo 2 — Distância Máxima de Visibilidade (D_max)
```
D_max = √[(2r·H_obs)/(1−k)] + √[(2r·H_turb)/(1−k)]
```
- `H_obs` = altura do observador (m)
- `H_turb` = altura total do aerogerador (m)
- `k` = coeficiente de refração (padrão: 0,13)

**Constante global:** r = 6.367.000 m (raio médio da Terra)
