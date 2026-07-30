import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. Configuração da Página e Tema CSS
# ==========================================
st.set_page_config(
    page_title="Dashboard: Redes Sociais & Saúde Mental",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS personalizada (Glassmorphism + Dark Mode Elegante)
st.markdown("""
<style>
    /* Estilo global */
    .main {
        background-color: #0e1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* Título principal */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #60a5fa 0%, #a855f7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }

    /* Cartões de Métricas (KPIs) */
    .kpi-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease-in-out;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: rgba(168, 85, 247, 0.4);
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 0.4rem;
    }
    .kpi-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-icon {
        font-size: 1.5rem;
        margin-bottom: 0.2rem;
    }

    /* Estilização das Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        white-space: pre-wrap;
        background-color: #1e293b;
        border-radius: 8px 8px 0px 0px;
        color: #94a3b8;
        font-weight: 600;
        padding: 0px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
    }
    
    /* Tabelas estilizadas */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. Carregamento dos Dados com Cache
# ==========================================
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        "Impacto_Redes_Sociais_e_Saude_Mental_Estudantes.csv",
        os.path.join(script_dir, "Impacto_Redes_Sociais_e_Saude_Mental_Estudantes.csv"),
        os.path.join("data", "Impacto_Redes_Sociais_e_Saude_Mental_Estudantes.csv"),
        os.path.join(script_dir, "data", "Impacto_Redes_Sociais_e_Saude_Mental_Estudantes.csv"),
        "Student Social Media And Mental Health Impact_pt_BR.csv",
        os.path.join(script_dir, "Student Social Media And Mental Health Impact_pt_BR.csv"),
        "Student Social Media And Mental Health Impact.csv",
        os.path.join(script_dir, "Student Social Media And Mental Health Impact.csv")
    ]
    
    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break
            
    if file_path is None:
        raise FileNotFoundError("Não foi possível encontrar o arquivo de dados CSV em nenhum dos caminhos previstos.")
        
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    
    # Garantir nomes de colunas em português caso o arquivo original tenha sido carregado
    column_mapping = {
        'Age': 'Idade',
        'Gender': 'Gênero',
        'Country': 'País',
        'Academic_Level': 'Nível_Acadêmico',
        'Most_Used_Platform': 'Plataforma_Mais_Usada',
        'Purpose_Of_Use': 'Propósito_de_Uso',
        'Avg_Daily_Usage_Hours': 'Horas_Médias_de_Uso_Diário',
        'Daily_Unlocks': 'Desbloqueios_Diários',
        'Study_Hours': 'Horas_de_Estudo',
        'Physical_Activity_Hours': 'Horas_de_Atividade_Física',
        'Sleep_Hours_Per_Night': 'Horas_de_Sono_por_Noite',
        'Stress_Level': 'Nível_de_Estresse',
        'Mental_Health_Score': 'Pontuação_de_Saúde_Mental'
    }
    df = df.rename(columns=column_mapping)
    return df

df_raw = load_data()


# ==========================================
# 3. Barra Lateral (Filtros Interativos)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3068/3068285.png", width=70)
st.sidebar.title("🔍 Filtros da Pesquisa")
st.sidebar.markdown("---")

# Filtro de Gênero
generos_disponiveis = df_raw['Gênero'].unique().tolist()
generos_selecionados = st.sidebar.multiselect(
    "Gênero",
    options=generos_disponiveis,
    default=generos_disponiveis
)

# Filtro de Nível Acadêmico
niveis_disponiveis = df_raw['Nível_Acadêmico'].unique().tolist()
niveis_selecionados = st.sidebar.multiselect(
    "Nível Acadêmico",
    options=niveis_disponiveis,
    default=niveis_disponiveis
)

# Filtro de Idade (Slider)
idade_min = int(df_raw['Idade'].min())
idade_max = int(df_raw['Idade'].max())
faixa_idade = st.sidebar.slider(
    "Faixa Etária (anos)",
    min_value=idade_min,
    max_value=idade_max,
    value=(idade_min, idade_max)
)

# Filtro de Plataforma
plataformas_disponiveis = df_raw['Plataforma_Mais_Usada'].unique().tolist()
plataformas_selecionadas = st.sidebar.multiselect(
    "Plataforma de Rede Social",
    options=plataformas_disponiveis,
    default=plataformas_disponiveis
)

# Filtro de País
paises_disponiveis = df_raw['País'].unique().tolist()
paises_selecionados = st.sidebar.multiselect(
    "País",
    options=paises_disponiveis,
    default=paises_disponiveis
)

# Aplicação dos filtros
df_filtered = df_raw[
    (df_raw['Gênero'].isin(generos_selecionados)) &
    (df_raw['Nível_Acadêmico'].isin(niveis_selecionados)) &
    (df_raw['Idade'] >= faixa_idade[0]) &
    (df_raw['Idade'] <= faixa_idade[1]) &
    (df_raw['Plataforma_Mais_Usada'].isin(plataformas_selecionadas)) &
    (df_raw['País'].isin(paises_selecionados))
]

st.sidebar.markdown("---")
st.sidebar.info(f"📊 **{len(df_filtered):,}** de **{len(df_raw):,}** registros selecionados.")


# ==========================================
# 4. Cabeçalho Principal
# ==========================================
st.markdown('<div class="main-title">📊 Impacto das Redes Sociais na Saúde Mental dos Estudantes</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Painel analítico interativo para investigação estatística do comportamento digital e bem-estar acadêmico.</div>', unsafe_allow_html=True)

if len(df_filtered) == 0:
    st.warning("⚠️ Nenhum registro encontrado para os filtros selecionados. Por favor, ajuste as opções na barra lateral.")
    st.stop()


# ==========================================
# 5. Módulos de Dashboards (Abas)
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 1. Visão Geral",
    "👤 2. Perfil dos Estudantes",
    "📱 3. Uso de Mídias Sociais",
    "🧠 4. Saúde Mental",
    "🏃 5. Hábitos de Vida",
    "🔄 6. Análises Comparativas",
    "🧮 7. Correlações",
    "🌍 8. Análises por País"
])

# Paleta de Cores Plotly Dark Theme
PLOTLY_TEMPLATE = "plotly_dark"
COLOR_PALETTE = px.colors.qualitative.Plotly


# ----------------------------------------------------
# TAB 1: VISÃO GERAL (DASHBOARD EXECUTIVO)
# ----------------------------------------------------
with tab1:
    st.subheader("📌 Indicadores Chave de Desempenho (KPIs)")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🎓</div>
            <div class="kpi-label">Estudantes</div>
            <div class="kpi-value">{len(df_filtered):,}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🎂</div>
            <div class="kpi-label">Média Idade</div>
            <div class="kpi-value">{df_filtered['Idade'].mean():.1f} <span style="font-size: 0.9rem;">anos</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📱</div>
            <div class="kpi-label">Uso Diário</div>
            <div class="kpi-value">{df_filtered['Horas_Médias_de_Uso_Diário'].mean():.1f} <span style="font-size: 0.9rem;">h/dia</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">🧠</div>
            <div class="kpi-label">Saúde Mental</div>
            <div class="kpi-value">{df_filtered['Pontuação_de_Saúde_Mental'].mean():.2f} <span style="font-size: 0.9rem;">/10</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">😴</div>
            <div class="kpi-label">Horas Sono</div>
            <div class="kpi-value">{df_filtered['Horas_de_Sono_por_Noite'].mean():.1f} <span style="font-size: 0.9rem;">h/noite</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">📚</div>
            <div class="kpi-label">Horas Estudo</div>
            <div class="kpi-value">{df_filtered['Horas_de_Estudo'].mean():.1f} <span style="font-size: 0.9rem;">h/dia</span></div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Resumo Geral Gráfico
    c1, c2 = st.columns(2)
    
    with c1:
        fig_summary1 = px.histogram(
            df_filtered, 
            x='Pontuação_de_Saúde_Mental', 
            color='Nível_de_Estresse',
            title="Distribuição da Saúde Mental por Nível de Estresse",
            template=PLOTLY_TEMPLATE,
            barmode="overlay",
            color_discrete_map={'Baixo': '#10b981', 'Médio': '#f59e0b', 'Alto': '#ef4444', 'Muito Alto': '#8b5cf6'}
        )
        fig_summary1.update_layout(margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_summary1, use_container_width=True)

    with c2:
        df_level_summary = df_filtered.groupby('Nível_Acadêmico')[
            ['Horas_Médias_de_Uso_Diário', 'Horas_de_Estudo', 'Horas_de_Sono_por_Noite']
        ].mean().reset_index()
        
        fig_summary2 = px.bar(
            df_level_summary, 
            x='Nível_Acadêmico', 
            y=['Horas_Médias_de_Uso_Diário', 'Horas_de_Estudo', 'Horas_de_Sono_por_Noite'],
            barmode='group',
            title="Média de Horas Diárias (Uso, Estudo, Sono) por Nível Acadêmico",
            template=PLOTLY_TEMPLATE,
            labels={'value': 'Horas', 'variable': 'Atividade'}
        )
        fig_summary2.update_layout(margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_summary2, use_container_width=True)


# ----------------------------------------------------
# TAB 2: PERFIL DOS ESTUDANTES
# ----------------------------------------------------
with tab2:
    st.subheader("👤 Perfil Demográfico da Amostra")
    
    r1_col1, r1_col2 = st.columns(2)
    
    with r1_col1:
        # Distribuição por Gênero
        df_gender = df_filtered['Gênero'].value_counts().reset_index()
        df_gender.columns = ['Gênero', 'Quantidade']
        fig_gender = px.pie(
            df_gender, 
            names='Gênero', 
            values='Quantidade', 
            title="Distribuição por Gênero",
            hole=0.4,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=['#3b82f6', '#ec4899', '#a855f7']
        )
        fig_gender.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_gender, use_container_width=True)

    with r1_col2:
        # Distribuição por Nível Acadêmico
        df_academic = df_filtered['Nível_Acadêmico'].value_counts().reset_index()
        df_academic.columns = ['Nível_Acadêmico', 'Quantidade']
        fig_academic = px.bar(
            df_academic, 
            x='Nível_Acadêmico', 
            y='Quantidade',
            color='Nível_Acadêmico',
            title="Distribuição por Nível Acadêmico",
            text='Quantidade',
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_academic.update_traces(textposition='outside')
        st.plotly_chart(fig_academic, use_container_width=True)

    # Distribuição por País
    st.markdown("---")
    top_n_countries = st.slider("Selecione a quantidade de países principais a exibir:", min_value=5, max_value=30, value=15)
    
    df_country = df_filtered['País'].value_counts().head(top_n_countries).reset_index()
    df_country.columns = ['País', 'Quantidade']
    
    fig_country = px.bar(
        df_country, 
        x='Quantidade', 
        y='País',
        orientation='h',
        title=f"Top {top_n_countries} Países com Maior Número de Estudantes na Pesquisa",
        color='Quantidade',
        color_continuous_scale='Viridis',
        template=PLOTLY_TEMPLATE,
        text='Quantidade'
    )
    fig_country.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_country, use_container_width=True)


# ----------------------------------------------------
# TAB 3: USO DAS MÍDIAS SOCIAIS
# ----------------------------------------------------
with tab3:
    st.subheader("📱 Padrões e Hábitos de Uso das Mídias Sociais")
    
    c1, c2 = st.columns(2)
    
    with c1:
        # Plataforma Mais Utilizada
        df_platform = df_filtered['Plataforma_Mais_Usada'].value_counts().reset_index()
        df_platform.columns = ['Plataforma', 'Quantidade']
        fig_platform = px.bar(
            df_platform, 
            x='Plataforma', 
            y='Quantidade',
            color='Plataforma',
            title="Plataformas Mais Utilizadas pelos Estudantes",
            text='Quantidade',
            template=PLOTLY_TEMPLATE
        )
        st.plotly_chart(fig_platform, use_container_width=True)

    with c2:
        # Propósito do Uso
        df_purpose = df_filtered['Propósito_de_Uso'].value_counts().reset_index()
        df_purpose.columns = ['Propósito', 'Quantidade']
        fig_purpose = px.pie(
            df_purpose, 
            names='Propósito', 
            values='Quantidade', 
            title="Finalidade Principal do Uso das Redes Sociais",
            hole=0.4,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_purpose, use_container_width=True)

    r2_c1, r2_c2 = st.columns(2)
    
    with r2_c1:
        # Histograma das Horas de Uso
        fig_usage_hist = px.histogram(
            df_filtered, 
            x='Horas_Médias_de_Uso_Diário',
            nbins=20,
            title="Histograma das Horas Diárias de Uso de Redes Sociais",
            labels={'Horas_Médias_de_Uso_Diário': 'Horas por Dia'},
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=['#8b5cf6']
        )
        st.plotly_chart(fig_usage_hist, use_container_width=True)

    with r2_c2:
        # Boxplot das Horas de Uso
        fig_usage_box = px.box(
            df_filtered, 
            y='Horas_Médias_de_Uso_Diário',
            x='Plataforma_Mais_Usada',
            color='Plataforma_Mais_Usada',
            title="Boxplot das Horas Diárias de Uso por Plataforma",
            template=PLOTLY_TEMPLATE
        )
        st.plotly_chart(fig_usage_box, use_container_width=True)


# ----------------------------------------------------
# TAB 4: SAÚDE MENTAL
# ----------------------------------------------------
with tab4:
    st.subheader("🧠 Indicadores e Avaliação de Saúde Mental")
    
    m1, m2 = st.columns(2)
    
    with m1:
        # Nível de Estresse
        df_stress = df_filtered['Nível_de_Estresse'].value_counts().reindex(['Baixo', 'Médio', 'Alto', 'Muito Alto']).reset_index()
        df_stress.columns = ['Nível de Estresse', 'Quantidade']
        fig_stress = px.bar(
            df_stress, 
            x='Nível de Estresse', 
            y='Quantidade',
            color='Nível de Estresse',
            title="Distribuição dos Níveis de Estresse",
            text='Quantidade',
            template=PLOTLY_TEMPLATE,
            color_discrete_map={'Baixo': '#10b981', 'Médio': '#f59e0b', 'Alto': '#ef4444', 'Muito Alto': '#8b5cf6'}
        )
        st.plotly_chart(fig_stress, use_container_width=True)

    with m2:
        # Histograma Pontuação de Saúde Mental
        fig_mh_hist = px.histogram(
            df_filtered, 
            x='Pontuação_de_Saúde_Mental',
            nbins=25,
            title="Histograma da Pontuação de Saúde Mental (0 a 10)",
            labels={'Pontuação_de_Saúde_Mental': 'Pontuação de Saúde Mental'},
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=['#06b6d4']
        )
        st.plotly_chart(fig_mh_hist, use_container_width=True)

    r2_m1, r2_m2 = st.columns(2)
    
    with r2_m1:
        # Boxplot por Gênero
        fig_box_gender = px.box(
            df_filtered, 
            x='Gênero', 
            y='Pontuação_de_Saúde_Mental',
            color='Gênero',
            title="Pontuação de Saúde Mental por Gênero",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=['#3b82f6', '#ec4899']
        )
        st.plotly_chart(fig_box_gender, use_container_width=True)

    with r2_m2:
        # Boxplot por Nível Acadêmico
        fig_box_academic = px.box(
            df_filtered, 
            x='Nível_Acadêmico', 
            y='Pontuação_de_Saúde_Mental',
            color='Nível_Acadêmico',
            title="Pontuação de Saúde Mental por Nível Acadêmico",
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_box_academic, use_container_width=True)


# ----------------------------------------------------
# TAB 5: HÁBITOS DE VIDA
# ----------------------------------------------------
with tab5:
    st.subheader("🏃 Rotina e Hábitos Diários dos Estudantes")
    
    hab_col1, hab_col2 = st.columns(2)
    
    with hab_col1:
        fig_sono = px.histogram(
            df_filtered, 
            x='Horas_de_Sono_por_Noite',
            title="Distribuição das Horas de Sono por Noite",
            nbins=20,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=['#6366f1']
        )
        st.plotly_chart(fig_sono, use_container_width=True)
        
        fig_estudo = px.histogram(
            df_filtered, 
            x='Horas_de_Estudo',
            title="Distribuição das Horas Diárias de Estudo",
            nbins=20,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=['#10b981']
        )
        st.plotly_chart(fig_estudo, use_container_width=True)

    with hab_col2:
        fig_atividade = px.histogram(
            df_filtered, 
            x='Horas_de_Atividade_Física',
            title="Distribuição das Horas Diárias de Atividade Física",
            nbins=20,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=['#f59e0b']
        )
        st.plotly_chart(fig_atividade, use_container_width=True)
        
        fig_unlocks = px.histogram(
            df_filtered, 
            x='Desbloqueios_Diários',
            title="Distribuição do Número de Desbloqueios do Celular",
            nbins=20,
            template=PLOTLY_TEMPLATE,
            color_discrete_sequence=['#ec4899']
        )
        st.plotly_chart(fig_unlocks, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Tabela de Estatísticas Descritivas dos Hábitos")
    stats_cols = ['Horas_de_Sono_por_Noite', 'Horas_de_Estudo', 'Horas_de_Atividade_Física', 'Desbloqueios_Diários']
    df_stats = df_filtered[stats_cols].describe().T[['mean', 'std', 'min', '50%', 'max']].reset_index()
    df_stats.columns = ['Variável', 'Média', 'Desvio Padrão', 'Mínimo', 'Mediana (50%)', 'Máximo']
    st.dataframe(df_stats.style.format({'Média': '{:.2f}', 'Desvio Padrão': '{:.2f}', 'Mínimo': '{:.1f}', 'Mediana (50%)': '{:.1f}', 'Máximo': '{:.1f}'}), use_container_width=True)


# ----------------------------------------------------
# TAB 6: ANÁLISES COMPARATIVAS
# ----------------------------------------------------
with tab6:
    st.subheader("🔄 Análises de Cruzamento de Variáveis")
    
    comp_c1, comp_c2 = st.columns(2)
    
    with comp_c1:
        # 1. Uso x Saúde Mental
        fig_scat1 = px.scatter(
            df_filtered, 
            x='Horas_Médias_de_Uso_Diário', 
            y='Pontuação_de_Saúde_Mental',
            color='Nível_de_Estresse',
            title="Horas de Uso Diário × Pontuação de Saúde Mental",
            trendline="ols",
            template=PLOTLY_TEMPLATE,
            color_discrete_map={'Baixo': '#10b981', 'Médio': '#f59e0b', 'Alto': '#ef4444', 'Muito Alto': '#8b5cf6'}
        )
        st.plotly_chart(fig_scat1, use_container_width=True)

    with comp_c2:
        # 2. Sono x Saúde Mental
        fig_scat2 = px.scatter(
            df_filtered, 
            x='Horas_de_Sono_por_Noite', 
            y='Pontuação_de_Saúde_Mental',
            color='Nível_de_Estresse',
            title="Horas de Sono × Pontuação de Saúde Mental",
            trendline="ols",
            template=PLOTLY_TEMPLATE,
            color_discrete_map={'Baixo': '#10b981', 'Médio': '#f59e0b', 'Alto': '#ef4444', 'Muito Alto': '#8b5cf6'}
        )
        st.plotly_chart(fig_scat2, use_container_width=True)

    comp_c3, comp_c4 = st.columns(2)
    
    with comp_c3:
        # 3. Atividade Física x Saúde Mental
        fig_scat3 = px.scatter(
            df_filtered, 
            x='Horas_de_Atividade_Física', 
            y='Pontuação_de_Saúde_Mental',
            color='Gênero',
            title="Horas de Atividade Física × Pontuação de Saúde Mental",
            trendline="ols",
            template=PLOTLY_TEMPLATE
        )
        st.plotly_chart(fig_scat3, use_container_width=True)

    with comp_c4:
        # 4. Horas de Estudo x Estresse
        fig_box_study_stress = px.box(
            df_filtered, 
            x='Nível_de_Estresse', 
            y='Horas_de_Estudo',
            color='Nível_de_Estresse',
            title="Horas de Estudo por Nível de Estresse",
            category_orders={'Nível_de_Estresse': ['Baixo', 'Médio', 'Alto', 'Muito Alto']},
            template=PLOTLY_TEMPLATE,
            color_discrete_map={'Baixo': '#10b981', 'Médio': '#f59e0b', 'Alto': '#ef4444', 'Muito Alto': '#8b5cf6'}
        )
        st.plotly_chart(fig_box_study_stress, use_container_width=True)

    # 5. Desbloqueios x Saúde Mental
    fig_scat5 = px.scatter(
        df_filtered, 
        x='Desbloqueios_Diários', 
        y='Pontuação_de_Saúde_Mental',
        color='Horas_Médias_de_Uso_Diário',
        title="Desbloqueios Diários do Celular × Pontuação de Saúde Mental (com gradiente de uso)",
        color_continuous_scale='Magma',
        trendline="ols",
        template=PLOTLY_TEMPLATE
    )
    st.plotly_chart(fig_scat5, use_container_width=True)


# ----------------------------------------------------
# TAB 7: CORRELAÇÕES
# ----------------------------------------------------
with tab7:
    st.subheader("🧮 Matriz de Correlação de Pearson")
    st.markdown("Mede a força e a direção da relação linear entre as variáveis quantitativas da pesquisa.")
    
    quant_cols = [
        'Idade',
        'Horas_Médias_de_Uso_Diário',
        'Desbloqueios_Diários',
        'Horas_de_Estudo',
        'Horas_de_Atividade_Física',
        'Horas_de_Sono_por_Noite',
        'Pontuação_de_Saúde_Mental'
    ]
    
    corr_matrix = df_filtered[quant_cols].corr()
    
    fig_corr = px.imshow(
        corr_matrix,
        text_auto='.2f',
        aspect="auto",
        color_continuous_scale='RdBu_r',
        title="Matriz de Correlação Interativa (Pearson r)",
        template=PLOTLY_TEMPLATE,
        range_color=[-1, 1]
    )
    fig_corr.update_layout(height=550)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.markdown("---")
    st.subheader("💡 Principais Insights de Correlação")
    
    # Exibir correlações ordenadas
    corr_unstacked = corr_matrix.unstack().reset_index()
    corr_unstacked.columns = ['Variável 1', 'Variável 2', 'Coeficiente (r)']
    corr_filtered = corr_unstacked[corr_unstacked['Variável 1'] != corr_unstacked['Variável 2']].copy()
    corr_filtered['Abs_r'] = corr_filtered['Coeficiente (r)'].abs()
    corr_sorted = corr_filtered.sort_values(by='Abs_r', ascending=False).drop_duplicates(subset=['Abs_r']).head(5)
    
    st.dataframe(
        corr_sorted[['Variável 1', 'Variável 2', 'Coeficiente (r)']].style.format({'Coeficiente (r)': '{:+.3f}'}),
        use_container_width=True
    )

# ----------------------------------------------------
# TAB 8: ANÁLISES POR PAÍS
# ----------------------------------------------------
with tab8:
    st.subheader("🌍 Análises Detalhadas por País")
    
    # Filtrar para os top 20 países com mais respondentes para os gráficos não ficarem poluídos
    top_paises = df_filtered['País'].value_counts().head(20).index
    df_top_paises = df_filtered[df_filtered['País'].isin(top_paises)]
    
    c1, c2 = st.columns(2)
    with c1:
        # Média de Saúde Mental por País
        df_country_mh = df_top_paises.groupby('País')['Pontuação_de_Saúde_Mental'].mean().sort_values().reset_index()
        fig_country_mh = px.bar(
            df_country_mh,
            x='Pontuação_de_Saúde_Mental',
            y='País',
            orientation='h',
            title="Média de Saúde Mental por País (Top 20)",
            color='Pontuação_de_Saúde_Mental',
            color_continuous_scale='Viridis',
            template=PLOTLY_TEMPLATE
        )
        st.plotly_chart(fig_country_mh, use_container_width=True)
        
    with c2:
        # Média de Horas de Uso por País
        df_country_usage = df_top_paises.groupby('País')['Horas_Médias_de_Uso_Diário'].mean().sort_values().reset_index()
        fig_country_usage = px.bar(
            df_country_usage,
            x='Horas_Médias_de_Uso_Diário',
            y='País',
            orientation='h',
            title="Horas Médias de Redes Sociais por País (Top 20)",
            color='Horas_Médias_de_Uso_Diário',
            color_continuous_scale='Plasma',
            template=PLOTLY_TEMPLATE
        )
        st.plotly_chart(fig_country_usage, use_container_width=True)
        
    # Boxplot de Saúde Mental por País
    fig_box_country = px.box(
        df_top_paises,
        x='País',
        y='Pontuação_de_Saúde_Mental',
        color='País',
        title="Distribuição da Saúde Mental por País (Top 20)",
        template=PLOTLY_TEMPLATE
    )
    fig_box_country.update_layout(xaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_box_country, use_container_width=True)

