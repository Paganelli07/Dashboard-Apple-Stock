import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("https://raw.githubusercontent.com/Paganelli07/DataFrame-filtrado-Apple/refs/heads/main/df_apple.csv")

st.set_page_config(
    page_title="Dashboard Análise das Ações da Apple",
    page_icon="📈",
    layout="wide",
)

# convert Data column
if not pd.api.types.is_datetime64_any_dtype(df['Data']):
    df['Data'] = pd.to_datetime(df['Data'])

# --- sidebar date filter ---
st.sidebar.markdown("---")
st.sidebar.title("Filtrar por intervalo de datas")

min_date = df['Data'].min().date()
max_date = df['Data'].max().date()

# two separate calendar widgets for start and end dates
start_date = st.sidebar.date_input(
    "Data inicial",
    value=min_date,
    min_value=min_date,
    max_value=max_date,
    key="start_date",
)
end_date = st.sidebar.date_input(
    "Data final",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
    key="end_date",
)

# ensure start_date is not after end_date
if start_date > end_date:
    st.sidebar.error("A data inicial não pode ser posterior à data final.")

filtered = df[(df['Data'].dt.date >= start_date) & (df['Data'].dt.date <= end_date)]

st.title("Apple Stock Dashboard")

col1, col2 = st.columns(2)
with col1:
    fig = px.line(filtered, x="Data", y="Fechamento", title="Preços das ações ao longo do tempo")
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Preço de Fechamento (USD)",
        title_x=0,
    )
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig2 = px.bar(filtered, x="Data", y="Volume", title="Volume de negócios ao longo do tempo")
    fig2.update_layout(
        xaxis_title="Data",
        yaxis_title="Volume de Negócios",
        title_x=0,
        
    )
    st.plotly_chart(fig2, use_container_width=True)

# summary columns
col3, col4 = st.columns(2)
with col3:
    st.subheader("Visão geral do preço das ações")
    initial_price = df.sort_values("Data")["Fechamento"].iloc[0]
    avg_2025 = df[df['Data'].dt.year == 2025]["Fechamento"].mean()
    max_price = df['Fechamento'].max()
    min_price = df['Fechamento'].min()
    st.metric("Preço inicial", f"${initial_price:.2f}")
    st.metric("Média 2025", f"${avg_2025:.2f}" if not pd.isna(avg_2025) else "N/A")
    st.metric("Preço máximo alcançado", f"${max_price:.2f}")
    st.metric("Preço mínimo alcançado", f"${min_price:.2f}")
with col4:
    df2025 = df[df['Data'].dt.year == 2025]
    if not df2025.empty:
        fig3 = px.line(df2025, x="Data", y="Fechamento", title="Preços em 2025")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.write("Sem dados para 2025")

# additional info row
col5, col6, col7 = st.columns(3)
with col5:
    st.subheader("Análise estatística")
    median_price = df['Fechamento'].median()
    last_price = df.sort_values('Data')['Fechamento'].iloc[-1]
    std_price = df['Fechamento'].std()
    st.metric("Mediana", f"${median_price:.2f}")
    st.metric("Último preço", f"${last_price:.2f}")
    st.metric("Desvio padrão", f"${std_price:.2f}")
with col6:
    st.subheader("Variação do retorno diário")
    avg_return = df['Retorno diário'].mean()
    max_return = df['Retorno diário'].max()
    min_return = df['Retorno diário'].min()
    st.metric("Retorno diário médio", f"{avg_return:.4f}")
    st.metric("Retorno diário máximo 🔼", f"{max_return:.4f}")
    st.metric("Retorno diário mínimo 🔽", f"{min_return:.4f}")
with col7:
    st.subheader("Desempenho geral")
    # another unique set of statistics with icons
    pos_days = (df['Retorno diário'] > 0).sum()
    neg_days = (df['Retorno diário'] < 0).sum()
    st.metric("Dias com retorno positivo ➕", f"{pos_days}")
    st.metric("Dias com retorno negativo ➖", f"{neg_days}")

# display filtered data below summaries
st.markdown("---")
st.markdown("### **DataFrame filtrado**")
# formatando as datas para exibição mais amigável
start_str = start_date.strftime("%b %d, %Y")
end_str = end_date.strftime("%b %d, %Y")
st.write(f"Mostrando {len(filtered)} linhas entre {start_str} e {end_str}.")
st.dataframe(filtered)
