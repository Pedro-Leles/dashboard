import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

st.title('Dashboard de Vendas')

@st.cache_data
def carregar_dados():
    df = pd.read_csv('vendas.csv')
    df['Data'] = pd.to_datetime(df['Data'])
    return df

df = carregar_dados()

st.sidebar.title('Filtros')

categorias_disponiveis = df['Categoria'].unique().tolist()

categorias_selecionadas = st.sidebar.multiselect(
    'Selecione as Categorias', 
    options=categorias_disponiveis,
    default=categorias_disponiveis
)

if categorias_selecionadas:
    df_filtrado = df[df['Categoria'].isin(categorias_selecionadas)]
else:
    df_filtrado = df.copy()

col1, col2 = st.columns([1, 1])

receita_total = df_filtrado['Valor'].sum()
total_pedidos = df_filtrado.shape[0]

with col1:
    st.metric(label='Receita Total', value=f"R$ {receita_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with col2:
    st.metric(label='Total de Pedidos', value=f"{total_pedidos:,}".replace(",", "."))

st.markdown("---")

aba1, aba2 = st.tabs(['Evolução Mensal', 'Tabela de Dados'])

with aba1:
    st.subheader('Evolução da Receita por Mês')
    
    df_mensal = df_filtrado.set_index('Data').resample('ME')['Valor'].sum().reset_index()
    df_mensal['Data'] = df_mensal['Data'].dt.strftime('%Y-%m')
    df_mensal = df_mensal.set_index('Data')
    
    st.area_chart(df_mensal['Valor'])

with aba2:
    st.subheader('Visão Detalhada dos Dados')
    
    st.dataframe(df_filtrado, use_container_width=True)
    
    csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Baixar Dados Filtrados em CSV",
        data=csv_data,
        file_name="vendas_filtradas.csv",
        mime="text/csv"
    )
