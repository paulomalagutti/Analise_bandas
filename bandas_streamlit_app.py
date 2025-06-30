import streamlit as st
from streamlit_option_menu import option_menu
from bandas_backend import (
    buscar_letras, 
    buscar_letra_musica_especifica,
    gerar_nuvem, 
    analise_sentimento, 
    interpretar_sentimento,
    buscar_dados_wikipedia,
    limpar_letra,
    extrair_palavras_principais,
    traduzir_palavras,
    sp
)
import pandas as pd
import plotly.express as px

def render_banda_analysis():
    st.title("Análise de Bandas")

    banda = st.text_input("Digite o nome da banda:")
    if banda:
        with st.spinner("Buscando informações..."):
            letras = buscar_letras(banda)
            if letras:
                st.subheader("Nuvem de Palavras")
                fig = gerar_nuvem(letras)
                st.pyplot(fig)

                st.subheader("Análise de Sentimento")
                sentimento_valor = analise_sentimento(letras)
                sentimento_txt, cor = interpretar_sentimento(sentimento_valor)
                st.markdown(f"**Sentimento:** <span style='color:{cor}'>{sentimento_txt}</span>", unsafe_allow_html=True)

                st.subheader("Palavras Mais Frequentes")
                palavras_freq = extrair_palavras_principais(letras)
                palavras_traduzidas = traduzir_palavras(palavras_freq)
                df_palavras = pd.DataFrame(palavras_traduzidas, columns=["Original", "Tradução", "Frequência"])
                st.dataframe(df_palavras)

                st.subheader("Resumo da Wikipedia")
                conteudo, imagem, vendas = buscar_dados_wikipedia(banda)
                st.markdown(conteudo)
                if imagem:
                    st.image(imagem, width=300)
                if vendas:
                    st.markdown("**Informações adicionais:**")
                    for v in vendas:
                        st.markdown(f"- {v}")
            else:
                st.warning("Não foram encontradas letras para essa banda.")

def render_musica_analysis():
    st.title("Análise de Música")

    nome_musica = st.text_input("Nome da música:")
    artista = st.text_input("Nome do artista (opcional):")

    if nome_musica:
        with st.spinner("Buscando letra..."):
            resultado = buscar_letra_musica_especifica(nome_musica, artista)
            if resultado:
                letra = resultado["letra"]
                st.subheader("Letra da Música")
                st.text(letra)

                st.subheader("Análise de Sentimento")
                sentimento_valor = analise_sentimento(letra)
                sentimento_txt, cor = interpretar_sentimento(sentimento_valor)
                st.markdown(f"**Sentimento:** <span style='color:{cor}'>{sentimento_txt}</span>", unsafe_allow_html=True)

                st.subheader("Nuvem de Palavras")
                fig = gerar_nuvem(letra)
                st.pyplot(fig)

                st.subheader("Palavras Mais Frequentes")
                palavras_freq = extrair_palavras_principais(letra)
                palavras_traduzidas = traduzir_palavras(palavras_freq)
                df_palavras = pd.DataFrame(palavras_traduzidas, columns=["Original", "Tradução", "Frequência"])
                st.dataframe(df_palavras)
            else:
                st.warning("Letra não encontrada.")

def render_racing_chart():
    st.title("Racing Chart - Músicas mais populares de uma banda")

    banda = st.text_input("Digite o nome da banda para ver ranking de popularidade:")

    if banda:
        with st.spinner("Buscando músicas..."):
            musicas = sp.search(q=banda, type="track", limit=20)["tracks"]["items"]

            if musicas:
                dados = []
                for item in musicas:
                    dados.append({
                        "Música": item["name"],
                        "Popularidade": item["popularity"]
                    })

                df = pd.DataFrame(dados).sort_values(by="Popularidade", ascending=True)

                fig = px.bar(
                    df,
                    x="Popularidade",
                    y="Música",
                    orientation="h",
                    title=f"Músicas mais populares de {banda}",
                    color="Popularidade",
                    color_continuous_scale="Viridis"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Nenhuma música encontrada.")

st.set_page_config(page_title="Analisador Musical", layout="wide")

selected = option_menu(
    menu_title=None,
    options=["🎤 Análise de Bandas", "🎵 Análise de Música", "🏆 Racing Chart", "ℹ️ Sobre"],
    icons=["music-note-beamed", "music-note", "trophy", "info-circle"],
    default_index=0,
    orientation="horizontal"
)

if selected == "🎤 Análise de Bandas":
    render_banda_analysis()

elif selected == "🎵 Análise de Música":
    render_musica_analysis()

elif selected == "🏆 Racing Chart":
    render_racing_chart()

elif selected == "ℹ️ Sobre":
    st.markdown("Feito com ❤️ usando Spotify, Lyrics.ovh, Wikipedia e Google Translate.")
