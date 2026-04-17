import streamlit as st
import time
import pandas as pd
import datetime
import graphviz
import selenium as webdriver
VENDAS = pd.read_excel(r"vendas_ficticias_5_lojas.xlsx")
opcao = st.sidebar.selectbox(
    "Escolha uma opção:",
    ["INICIO","valor venda","quantidade venda","meta de venda"]
    )
if opcao == "INICIO":
    st.write("Você escolheu:", opcao)
    st.title("INICIO: Boa supermercados")
    st.subheader('Analise geral de dados abaixo')
    st.image(
    "https://epgrupo.com.br/wp-content/uploads/2025/01/Boa-Samuel-Fachada-1920x1080.jpg",
    caption="Boa Supermercados",
    width=800
    )
    st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjvwDsniTVrhotAnJ_iQJSUMDVTAtIF-7y7uP2d-quKMLwmihUse0FgJP97IF19fmRYCZSuqIipP_JgkpHl27nUXWVMVD3J_luv3i8brhsNYkgIFz8dO5Rcs7rrrYbBgJsfNGf1n6L-kpUygwo6Twa1G0xi07JGNX5wGYaVuSFjXNzIu0OCk70jY4JY5RY/s600-rw/Captura%20de%20Tela%202024-12-18%20%C3%A0s%2019.48.40.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.set_page_config("inicio: dados gerais","📈","wide",initial_sidebar_state=400)
    VENDAS['numero da loja'] = VENDAS['numero da loja'].astype(str)
    VENDAS['categoria'] = VENDAS['categoria'].astype(str)  
    lojas = VENDAS['numero da loja'].dropna().unique()

    lojas_sel = st.multiselect("Filtrar por loja", lojas, default=lojas)
    CATEGORASELECIONADA = st.multiselect("Selecione a categoria", VENDAS['categoria'].unique())
    dados_filtrados = VENDAS[VENDAS['numero da loja'].isin(lojas_sel) & VENDAS['categoria'].isin(CATEGORASELECIONADA)]

    st.subheader("vendas filtradas")
    st.write(dados_filtrados)
    VENDAS['data'] = pd.to_datetime(VENDAS['data'], errors='coerce')
    st.datetime_input("coloque a data via calendario")
    st.balloons()
    st.subheader("vendas geral")
    st.write(VENDAS)
    INFOVENDAS30 = VENDAS.info()
    st.subheader("informações venda")
    st.write(INFOVENDAS30)
    maximovendas30 = VENDAS.max()
    minvendas30 = VENDAS.min()
    primeiraslinhasvendas30 = VENDAS.head(10)
    st.subheader("maior valor venda")
    st.write(maximovendas30)
    st.subheader("minimo valor de venda")
    st.write(minvendas30)
    st.subheader("primeiras linhas de venda")
    st.write(primeiraslinhasvendas30)
    contagemderegistros = VENDAS.count()
    st.subheader("contagem registros venda")
    st.write(contagemderegistros)
    st.status("dados carregados")
    vendas30media = VENDAS['meta de venda'].mean()
    st.subheader("media de venda 30")
    st.write(vendas30media)
    uploaded_file = st.file_uploader("Faça upload de um arquivo", type=["csv", "xlsx"])
    st.subheader("assinatura: time de io")
elif opcao == "meta de venda":
    st.set_page_config("DADOS: meta venda", "📈", layout="wide")

    st.title('Análise geral de dados em relação à Meta de Venda')
    st.subheader("Painel de análise")


    VENDAS['data'] = pd.to_datetime(VENDAS['data'], errors='coerce')
    VENDAS['numero da loja'] = VENDAS['numero da loja'].astype(str)
    VENDAS['categoria'] = VENDAS['categoria'].astype(str)

    lojas = VENDAS['numero da loja'].dropna().unique()
    CATEGORASELECIONADA = st.multiselect("Selecione a categoria", VENDAS['categoria'].unique())   
    lojas_sel = st.multiselect(
    "Filtrar por loja",
    lojas,
    default=lojas
    )

    dados_filtrados = VENDAS[
    (VENDAS['numero da loja'].isin(lojas_sel)) &
    (VENDAS['categoria'].isin(CATEGORASELECIONADA))
    ]
    
# =========================
# GRAFICO FLUXO
# =========================
    grafico = graphviz.Digraph()
    grafico.node('A', 'Carregar Dados')
    grafico.node('B', 'Filtrar')
    grafico.node('C', 'Analisar')
    grafico.node('D', 'Resultados')
    grafico.edges(['AB', 'BC', 'CD'])

    st.graphviz_chart(grafico)

    st.subheader("Meta de Vendas por Loja")
    dados = dados_filtrados.set_index('numero da loja') 
    st.bar_chart(dados["meta de venda"])

    st.subheader("Meta de Venda por Categoria")
    dados = dados_filtrados.set_index('categoria')
    st.bar_chart(dados["meta de venda"])

    st.subheader("Média por Loja")
    media_loja = dados_filtrados.groupby('numero da loja')['meta de venda'].mean()
    st.bar_chart(media_loja)

    st.subheader("Média por Categoria")
    media_cat = dados_filtrados.groupby('categoria')['meta de venda'].mean()
    st.bar_chart(media_cat)

    st.success("Dados carregados com sucesso")

    uploaded_file = st.file_uploader("Faça upload de um arquivo", type=["csv", "xlsx"])
elif opcao == "quantidade venda":
    st.set_page_config("DADOS DE QTD DE VENDA", "📈", layout="wide")

    st.title('Análise geral de dados em relação à Quantidade de Venda')
    st.subheader("Painel de análise")
    VENDAS['categoria'] = VENDAS['categoria'].astype(str)
    VENDAS['numero da loja'] = VENDAS['numero da loja'].astype(str)

    lojas = VENDAS['numero da loja'].dropna().unique()

    lojas_sel = st.multiselect(
    "Filtrar por loja",
    lojas,
    default=lojas
    )

    CATEGORASELECIONADA = st.multiselect("Selecione a categoria", VENDAS['categoria'].unique())
    dados_filtrados = VENDAS[
        (VENDAS['numero da loja'].isin(lojas_sel)) &
        (VENDAS['categoria'].isin(CATEGORASELECIONADA))
    ]


    VENDAS['data'] = pd.to_datetime(VENDAS['data'], errors='coerce')

    data_inicio, data_fim = st.date_input(
    "Selecione o período:",
    [dados_filtrados['data'].min(), dados_filtrados['data'].max()],
    key="filtro_data_qtd"
    )

    dados_filtrados = dados_filtrados[
    (dados_filtrados['data'] >= pd.to_datetime(data_inicio)) &
    (dados_filtrados['data'] <= pd.to_datetime(data_fim))
    ]

    grafico = graphviz.Digraph()
    grafico.node('A', 'Carregar Dados')
    grafico.node('B', 'Filtrar Dados')
    grafico.node('C', 'Analisar')
    grafico.node('D', 'Resultados')
    grafico.edges(['AB', 'BC', 'CD'])

    st.graphviz_chart(grafico)


    st.subheader("Quantidade de Vendas por Loja")
    dados = dados_filtrados.set_index('numero da loja')
    st.bar_chart(dados['quantidade venda'])

    st.subheader("Quantidade de Vendas por Categoria")
    dados = dados_filtrados.set_index('categoria')
    st.bar_chart(dados['quantidade venda'])

    st.subheader("Média por Loja")
    media_loja = dados_filtrados.groupby('numero da loja')['quantidade venda'].mean()
    st.bar_chart(media_loja)

    st.subheader("Média por Categoria")
    media_cat = dados_filtrados.groupby('categoria')['quantidade venda'].mean()
    st.bar_chart(media_cat)

    st.success("Dados carregados com sucesso")
elif opcao == "valor venda":
    st.set_page_config("Dados: valor venda", "📈", layout="wide")

    st.title('Análise geral de dados em relação ao Valor de Venda')
    st.subheader("Painel de análise")

    VENDAS['categoria'] = VENDAS['categoria'].astype(str)
    VENDAS['numero da loja'] = VENDAS['numero da loja'].astype(str)
    VENDAS['data'] = pd.to_datetime(VENDAS['data'], errors='coerce')

    CATEGORASELECIONADA = st.multiselect("Selecione a categoria", VENDAS['categoria'].unique())
# garantir tipos corretos ANTES de tudo
    VENDAS['numero da loja'] = VENDAS['numero da loja'].astype(str)
    VENDAS['data'] = pd.to_datetime(VENDAS['data'], errors='coerce')

# filtro de loja
    lojas = VENDAS['numero da loja'].dropna().unique()

    lojas_sel = st.multiselect(
    "Filtrar por loja",
    lojas,
    default=lojas,
    key="filtro_loja_valor"
    )

    dados_filtrados = VENDAS[
        (VENDAS['numero da loja'].isin(lojas_sel)) &
        (VENDAS['categoria'].isin(CATEGORASELECIONADA))
    ]

# filtro de data
    data_inicio, data_fim = st.date_input(
    "Selecione o período:",
    [dados_filtrados['data'].min(), dados_filtrados['data'].max()],
    key="filtro_data_valor"
    )

    dados_filtrados = dados_filtrados[
    (dados_filtrados['data'] >= pd.to_datetime(data_inicio)) &
    (dados_filtrados['data'] <= pd.to_datetime(data_fim))
    ]

# =========================
# GRAFICO FLUXO
# =========================
    grafico = graphviz.Digraph()
    grafico.node('A', 'Carregar Dados')
    grafico.node('B', 'Filtrar')
    grafico.node('C', 'Analisar')
    grafico.node('D', 'Resultados')
    grafico.edges(['AB', 'BC', 'CD'])

    st.graphviz_chart(grafico)

# =========================
# GRÁFICOS (SEMPRE dados_filtrados)
# =========================

    st.subheader("Valor de Venda por Loja")
    dados = dados_filtrados.set_index('numero da loja')
    st.bar_chart(dados['valor venda'])

    st.subheader("Valor de Venda por Categoria")
    dados = dados_filtrados.set_index('categoria')
    st.bar_chart(dados['valor venda'])

    st.subheader("Média por Loja")
    media_loja = dados_filtrados.groupby('numero da loja')['valor venda'].mean()
    st.bar_chart(media_loja)

    st.subheader("Média por Categoria")
    media_cat = dados_filtrados.groupby('categoria')['valor venda'].mean()
    st.bar_chart(media_cat)

    st.success("Dados carregados com sucesso")