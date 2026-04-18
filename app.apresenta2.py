import streamlit as st
import time
import pandas as pd
import datetime
import graphviz
import selenium as webdriver
import base64
from datetime import datetime
import streamlit.components.v1 as components
VENDAS = pd.read_excel(r"vendas_ficticias_5_lojas.xlsx")
st.set_page_config("LOGIN:BOA", "📈", layout="centered")
if "logado" not in st.session_state:
    st.session_state.logado = False

    st.markdown( """ <style> .stApp { background-image: url(""); background-size: cover; background-position: center; background-repeat: no-repeat; } </style> """, unsafe_allow_html=True)   
# tela de login
if not st.session_state.logado:
    st.title("Login: Boa Supermercados")
    st.markdown( """ <style> .stApp { background-image: url("https://epgrupo.com.br/wp-content/uploads/2025/01/Boa-Samuel-Fachada-scaled.jpg"); background-size: cover; background-position: center; background-repeat: no-repeat; } </style> """, unsafe_allow_html=True)
    
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario == "BOA.io" and senha == "Inteligencia@1110":
            st.session_state.logado = True
            st.success("Login bem-sucedido!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
    st.stop()

opcao = st.sidebar.selectbox(
    "Escolha uma opção:",
    ["INICIO","valor venda","quantidade venda","meta de venda","informaçoes app"]
    )
if opcao == "INICIO":
    st.write("Você escolheu:", opcao)
    st.title("INICIO: Boa supermercados")
    st.subheader('Analise geral de dados abaixo')
    st.image(
    "https://mir-s3-cdn-cf.behance.net/projects/max_808/c97177162211407.Y3JvcCwyMDEzLDE1NzUsMTA0MSwzNzg.jpg",
    caption="Boa Supermercados",
    width=280,
    clamp=True,
    channels="RGB",
    output_format="auto",
    use_container_width=False,
    )
    st.markdown(
    '<a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" target="_blank">Assistir no YouTube</a>',
    unsafe_allow_html=True
    )
    
    st.markdown( """ <style> .stApp { background-image: url("https://epgrupo.com.br/wp-content/uploads/2025/01/Boa-Samuel-Fachada-scaled.jpg"); background-size: cover; background-position: center; background-repeat: no-repeat; } </style> """, unsafe_allow_html=True)
    st.set_page_config("inicio: dados gerais","📈","wide",initial_sidebar_state=400)
    st.write("TESTE ATUALIZOU AGORA")
    
    VENDAS['numero da loja'] = VENDAS['numero da loja'].astype(str)
    VENDAS['categoria'] = VENDAS['categoria'].astype(str)  
    lojas = VENDAS['numero da loja'].dropna().unique()
    lojas_sel = st.multiselect("Filtrar por loja", lojas, default=lojas)
    CATEGORASELECIONADA = st.multiselect("Selecione a categoria", VENDAS['categoria'].unique(), default=VENDAS['categoria'].unique())
    dados_filtrados = VENDAS[VENDAS['numero da loja'].isin(lojas_sel) & VENDAS['categoria'].isin(CATEGORASELECIONADA)]

    st.subheader("vendas filtradas")
    st.write(dados_filtrados)
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
    st.subheader("media de vendas")
    st.write(vendas30media)
    st.subheader("descrição geral de vendas")
    st.table(VENDAS.describe())
    uploaded_file = st.file_uploader("Faça upload de um arquivo", type=["csv", "xlsx"])
    
    st.subheader("assinatura: time de io")
elif opcao == "meta de venda":
    st.set_page_config("DADOS: meta venda", "📈", layout="wide")

    st.title('Análise geral de dados em relação à Meta de Venda')
    st.subheader("Painel de análise")
    st.markdown( """ <style> .stApp { background-image: url("https://epgrupo.com.br/wp-content/uploads/2025/01/Boa-Samuel-Fachada-scaled.jpg"); background-size: cover; background-position: center; background-repeat: no-repeat; } </style> """, unsafe_allow_html=True)

    VENDAS['numero da loja'] = VENDAS['numero da loja'].astype(str)
    VENDAS['categoria'] = VENDAS['categoria'].astype(str)

    lojas = VENDAS['numero da loja'].dropna().unique()
    CATEGORASELECIONADA = st.multiselect("Selecione a categoria", VENDAS['categoria'].unique(), default=VENDAS['categoria'].unique())   
    lojas_sel = st.multiselect(
    "Filtrar por loja",
    lojas,
    default=lojas
    )
    dados_filtrados = VENDAS[
    (VENDAS['numero da loja'].isin(lojas_sel)) &
    (VENDAS['categoria'].isin(CATEGORASELECIONADA)) &
    (VENDAS['data'] == pd.to_datetime(VENDAS['data']))
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
    uploaded_file = st.file_uploader("Faça upload de um arquivo", type=["csv", "xlsx"])
    st.success("Dados carregados com sucesso")
elif opcao == "quantidade venda":
    st.set_page_config("DADOS DE QTD DE VENDA", "📈", layout="wide")

    st.title('Análise geral de dados em relação à Quantidade de Venda')
    st.subheader("Painel de análise")
    VENDAS['categoria'] = VENDAS['categoria'].astype(str)
    VENDAS['numero da loja'] = VENDAS['numero da loja'].astype(str)
    st.markdown( """ <style> .stApp { background-image: url("https://epgrupo.com.br/wp-content/uploads/2025/01/Boa-Samuel-Fachada-scaled.jpg"); background-size: cover; background-position: center; background-repeat: no-repeat; } </style> """, unsafe_allow_html=True)
    lojas = VENDAS['numero da loja'].dropna().unique()
    CATEGORASELECIONADA = st.multiselect("Selecione a categoria", VENDAS['categoria'].unique(), default=VENDAS['categoria'].unique())
    lojas_sel = st.multiselect(
    "Filtrar por loja",
    lojas,
    default=lojas
    )

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
    uploaded_file = st.file_uploader("Faça upload de um arquivo", type=["csv", "xlsx"])
    st.success("Dados carregados com sucesso")
elif opcao == "valor venda":
    st.set_page_config("Dados: valor venda", "📈", layout="wide")

    st.title('Análise geral de dados em relação ao Valor de Venda')
    st.subheader("Painel de análise")
    st.markdown( """ <style> .stApp { background-image: url("https://epgrupo.com.br/wp-content/uploads/2025/01/Boa-Samuel-Fachada-scaled.jpg"); background-size: cover; background-position: center; background-repeat: no-repeat; } </style> """, unsafe_allow_html=True)
    VENDAS['categoria'] = VENDAS['categoria'].astype(str)
    VENDAS['numero da loja'] = VENDAS['numero da loja'].astype(str)
    VENDAS['data'] = pd.to_datetime(VENDAS['data'], errors='coerce')

    CATEGORASELECIONADA = st.multiselect("Selecione a categoria", VENDAS['categoria'].unique(), default=VENDAS['categoria'].unique())

    VENDAS['numero da loja'] = VENDAS['numero da loja'].astype(str)
    VENDAS['data'] = pd.to_datetime(VENDAS['data'], errors='coerce')


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

    data_inicio, data_fim = st.date_input(
    "Selecione o período:",
    [dados_filtrados['data'].min(), dados_filtrados['data'].max()],
    key="filtro_data_valor"
    )

    dados_filtrados = dados_filtrados[
    (dados_filtrados['data'] >= pd.to_datetime(data_inicio)) &
    (dados_filtrados['data'] <= pd.to_datetime(data_fim))
    ]

    grafico = graphviz.Digraph()
    grafico.node('A', 'Carregar Dados')
    grafico.node('B', 'Filtrar')
    grafico.node('C', 'Analisar')
    grafico.node('D', 'Resultados')
    grafico.edges(['AB', 'BC', 'CD'])

    st.graphviz_chart(grafico)

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
    uploaded_file = st.file_uploader("Faça upload de um arquivo", type=["csv", "xlsx"])
    st.success("Dados carregados com sucesso")
elif opcao == "informaçoes app":
    st.title("Informações do App")
    st.markdown( """ <style> .stApp { background-image: url("https://epgrupo.com.br/wp-content/uploads/2025/01/Boa-Samuel-Fachada-scaled.jpg"); background-size: cover; background-position: center; background-repeat: no-repeat; } </style> """, unsafe_allow_html=True)
    st.subheader("Sobre o App")
    st.write("Este aplicativo foi desenvolvido para analisar os dados de vendas da Boa Supermercados. Ele permite que os usuários explorem diferentes aspectos das vendas, como valor, quantidade e metas, por loja e categoria.")
    st.subheader("Funcionalidades")
    st.write("- Análise de valor de venda por loja e categoria")
    st.write("- Análise de quantidade de venda por loja e categoria")
    st.write("- Análise de metas de venda por loja e categoria")
    st.write("- Filtros avançados por loja, categoria e período")
    st.subheader("Equipe de Desenvolvimento")
    st.write("Este aplicativo foi desenvolvido pela equipe de Inteligência do Boa Supermercados, com o objetivo de fornecer insights valiosos para a tomada de decisões estratégicas.")
    st.subheader("Contato")
    st.write("Para dúvidas, sugestões ou feedback, entre em contato conosco através do email: joao.altafini@smboa.com.br")
