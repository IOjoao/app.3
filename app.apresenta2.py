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
    st.set_page_config("inicio: dados gerais","📈","wide",initial_sidebar_state=400)
    st.title("INICIO: PAGINA INICIAL")
    st.title('Analise geral de dados a abaixo em realação a dados de vendas')
    st.subheader("ao lado um ainel com todas as informações do arquivo:")
    st.subheader("vendas 30 visualização logo abaixo")
    st.date_input("coloque sua data aqui embaixo:")
    
    lojas = VENDAS['numero da loja'].dropna().unique()

    lojas_sel = st.multiselect(
    "Filtrar por loja",
    lojas,
    default=lojas
    )
    st.datetime_input("coloque a data via calendario")
    st.selectbox("selecione as opções a seguir",["data","numero da loja"])
    st.number_input("digite aqui o numero da loja dos dados separadamenete",min_value=1, max_value=30)
    st.balloons()
    st.subheader("vendas geral")
    st.write(VENDAS)
    INFOVENDAS30 = VENDAS.info()
    st.subheader("informações de venda")
    st.write(INFOVENDAS30)
    maximovendas30 = VENDAS.max()
    minvendas30 = VENDAS.min()
    primeiraslinhasvendas30 = VENDAS.head(10)
    st.subheader("maior valor de vanda")
    st.write(maximovendas30)
    st.subheader("minimode valor de venda")
    st.write(minvendas30)
    st.subheader("primeiras linhas de venda")
    st.write(primeiraslinhasvendas30)
    contagemderegistros = VENDAS.count()
    st.subheader("contagem de registros na venda")
    st.write(contagemderegistros)
    st.status("dados carregados")
    vendas30media = VENDAS['meta de venda'].mean()
    st.subheader("media de venda 30")
    st.write(vendas30media)
    uploaded_file = st.file_uploader("Faça upload de um arquivo", type=["csv", "xlsx"])
    st.subheader("assinatura: time de io")
elif opcao == "meta de venda":
    st.set_page_config("DADOs: meta venda","📈",layout="wide")
    st.title('Analise geral de dados a abaixo em realação ao meta venda')
    st.subheader("aolado um ainel com todas as informações do arquivo:")
    st.subheader("Fluxo de análise das Analise")
    
    lojas = VENDAS['numero da loja'].dropna().unique()

    lojas_sel = st.multiselect(
    "Filtrar por loja",
    lojas,
    default=lojas
    )
    grafico = graphviz.Digraph()

    grafico.node('A', 'Carregar Dados')
    grafico.node('B', 'Analisar Vendas')
    grafico.node('C', 'Calcular Média')
    grafico.node('D', 'Exibir Resultados')

    grafico.edges(['AB', 'BC', 'CD'])
    VENDAS['data'] = pd.to_datetime(VENDAS['data'], errors='coerce')

    data_inicio, data_fim = st.date_input(
    "Selecione o período:",
    [VENDAS['data'].min(), VENDAS['data'].max()],
    key="filtro_data"
    )

    dados_filtrados = VENDAS[
    (VENDAS['data'] >= pd.to_datetime(data_inicio)) &
    (VENDAS['data'] <= pd.to_datetime(data_fim))
    ]
    st.graphviz_chart(grafico)


    st.subheader("Meta de Vendas por Loja")

    dados = dados_filtrados.set_index('numero da loja')
    st.bar_chart(dados["meta de venda"])
    st.subheader("Meta venda por categoria")
    dados = dados_filtrados.set_index("categoria")
    st.bar_chart(dados["meta de venda"])
    st.subheader("Média por loja")

    media_cat = dados_filtrados.groupby('numero da loja')['meta de venda'].mean()
    st.bar_chart(media_cat)
    st.success("dados carregados")
    #
    st.subheader("Média por categoria")

    media_cat = dados_filtrados.groupby('categoria')['meta de venda'].mean()
    st.bar_chart(media_cat)
    st.success("dados carregado")
    uploaded_file = st.file_uploader("Faça upload de um arquivo", type=["csv", "xlsx"])
    st.subheader("assinatura: time de io")
elif opcao == "quantidade venda":
    st.set_page_config("DADOS DE QTD DE VENDA","📈",layout="wide")
    st.title('Analise geral dade dados a abaixo em realação ao Quantidade - Venda')
    st.subheader("aolado um ainel com todas as informações do arquivo:")
    st.subheader("Fluxo de análise das  Analises")

    lojas = VENDAS['numero da loja'].dropna().unique()

    lojas_sel = st.multiselect(
    "Filtrar por loja",
    lojas,
    default=lojas
    )
    grafico = graphviz.Digraph()
    grafico.node('A', 'Carregar Dados')
    grafico.node('B', 'Analisar Vendas')
    grafico.node('C', 'Calcular Média')
    grafico.node('D', 'Exibir Resultados')
    grafico.edges(['AB', 'BC', 'CD'])
    VENDAS['data'] = pd.to_datetime(VENDAS['data'], errors='coerce')

    data_inicio, data_fim = st.date_input(
    "Selecione o período:",
    [VENDAS['data'].min(), VENDAS['data'].max()],
    key="filtro_data"
    )
    st.graphviz_chart(grafico)
    dados_filtrados = VENDAS[
    (VENDAS['data'] >= pd.to_datetime(data_inicio)) &
    (VENDAS['data'] <= pd.to_datetime(data_fim))
    ]
    st.graphviz_chart(grafico)

    st.subheader("Quantidade de Vendas por Loja")
    dados = dados_filtrados.set_index('numero da loja')
    st.bar_chart(dados['quantidade venda'])

    st.success("carregado com sucesso")
    st.subheader("Quantidade de Vendas por categoria")
    dados = dados_filtrados.set_index('categoria')
    st.bar_chart(dados['quantidade venda'])
    st.subheader("Média por loja")

    media_cat = dados_filtrados.groupby('numero da loja')['quantidade venda'].mean()
    st.bar_chart(media_cat)
    st.success("dados carregados")
    #
    st.subheader("Média por categoria")

    media_cat = dados_filtrados.groupby('categoria')['quantidade venda'].mean()
    st.bar_chart(media_cat)
    uploaded_file = st.file_uploader("Faça upload de um arquivo", type=["csv", "xlsx"])
    st.success("dados carregado")
    st.subheader("assinatura: time de io")
elif opcao == "valor venda":
    st.set_page_config("Dados: valor venda","📈",layout="wide")
    st.title('Analise geral de dados a abaixo em realação ao Valor - Venda')
    st.subheader("ao lado um ainel com todas as informações do arquivo:")
    st.subheader("Fluxo de análise das Analise")
    
    lojas = VENDAS['numero da loja'].dropna().unique()

    lojas_sel = st.multiselect(
    "Filtrar por loja",
    lojas,
    default=lojas
    )
    grafico = graphviz.Digraph()
    grafico.node('A', 'Carregar Dados')
    grafico.node('B', 'Analisar Vendas')
    grafico.node('C', 'Calcular Média')
    grafico.node('D', 'Exibir Resultados')
    grafico.edges(['AB', 'BC', 'CD'])
    VENDAS['data'] = pd.to_datetime(VENDAS['data'], errors='coerce')

    data_inicio, data_fim = st.date_input(
    "Selecione o período:",
    [VENDAS['data'].min(), VENDAS['data'].max()],
    key="filtro_data"
    )
    st.graphviz_chart(grafico)
    dados_filtrados = VENDAS[
    (VENDAS['data'] >= pd.to_datetime(data_inicio)) &
    (VENDAS['data'] <= pd.to_datetime(data_fim))
    ]
    st.graphviz_chart(grafico)

    st.subheader("Valor - Venda por Loja")
    dados = dados_filtrados.set_index('numero da loja')
    st.bar_chart(dados['valor venda'])

    st.success("carregado com sucesso")
    st.subheader("Valor - Venda por categoria")
    dados = dados_filtrados.set_index('categoria')
    st.bar_chart(dados['valor venda'])
    st.success("dados carregados")
    st.subheader("Média por loja")

    media_cat = dados_filtrados.groupby('numero da loja')['valor venda'].mean()
    st.bar_chart(media_cat)
    st.success("dados carregados")
    #
    st.subheader("Média por categoria")

    media_cat = dados_filtrados.groupby('categoria')['valor venda'].mean()
    st.bar_chart(media_cat)
    uploaded_file = st.file_uploader("Faça upload de um arquivo", type=["csv", "xlsx"])
    st.success("dados carregado")
    st.subheader("assinatura: Time de io")