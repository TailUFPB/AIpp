import streamlit as st
import pandas as pd
from PIL import Image

# Page configs
st.set_page_config(
    page_title='AIpp',
    page_icon='🤖',
)

# Creating the sidebar
st.sidebar.success("Selecione uma pagina acima!")

df = pd.read_csv("data/games_sentiment.csv")
app_tags = pd.read_csv("data/app_tags.csv")
df.sort_values('likes', inplace=True, ascending=False)

bot = Image.open('images/bot.png')

st.markdown("<h1 style='text-align: center;'>AIpp</h1>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col3.image(bot, use_column_width=True)
# st.image(bot, width=300, use_column_width=False)

def speech_balloon(text):
    col2.markdown(f'<div class="speech-balloon" >{text}</div>', unsafe_allow_html=True)
# CSS para estilizar o balão de fala
st.markdown(
    """
    <style>
    .speech-balloon {
        position: relative;
        background-color: #f9f9f9;
        color: black;
        margin: 50px 10px 0 20px;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .speech-balloon::after {
        content: '';
        position: absolute;
        border-style: solid;
        border-width: 20px 20px 0 0;
        border-color: #f9f9f9 transparent transparent transparent;
        right: -20px;
        top: 50%;
        transform: translateY(-50%);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Texto do balão
texto_balao = """\
<b>Olá, eu sou o AIpp, seu assistente pessoal para análise de sentimentos de aplicativos.</b>\n
<i>Selecione um aplicativo no menu abaixo para ver o dashboard.</i>
"""

speech_balloon(texto_balao)

# Estilos CSS
st.markdown("""
<style>
    .comments-container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
    
    .comments-list {
        list-style-type: disc;
        margin-left: 20px;
        padding-left: 10px;
    }
    
    .comments-div {
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

option = st.selectbox(
    'Qual App você deseja analisar?',
    df['app_name'].value_counts().index.tolist()
)

df = df[df['app_name'] == option]
app_tags = app_tags[[option, 'sentiment']] #Dataframe com as tags positivas e negativas dos apps

div_positive_tags = "<div class='tags-div' style='flex: 1; min-width: 0;'>"
div_positive_tags += "<h4>Positivas:</h4>"
div_positive_tags += "<ul class='tags-list'>"

app_pos_tags = app_tags.loc[app_tags['sentiment'] == 1][option] #Separa as tags positivas
app_pos_tags = list(app_pos_tags.values)

for item in app_pos_tags:
    item = eval(item)
    div_positive_tags += f"<li>{item[0].capitalize()}</li>"

div_positive_tags += "</ul>"
div_positive_tags += "</div>"

div_negative_tags = "<div class='tags-div' style='flex: 1; min-width: 0;'>"
div_negative_tags += "<h4>Negativas:</h4>"
div_negative_tags += "<ul class='tags-list'>"

app_neg_tags = app_tags.loc[app_tags['sentiment'] == 0][option] #Separa as tags negativas
app_neg_tags = list(app_neg_tags.values)

for item in app_neg_tags:
    item = eval(item)
    div_negative_tags += f"<li>{item[0].capitalize()}</li>"

div_negative_tags += "</ul>"
div_negative_tags += "</div>"

div_tags = "<div style='display: flex; padding: 10px;'>"
div_tags += div_positive_tags
div_tags += div_negative_tags
div_tags += "</div>"
st.markdown(div_tags, unsafe_allow_html=True)

df = df.head()
positive = df['positive_sentences']
negative = df['negative_sentences']

# Exibição dos comentários
div_positive = "<div class='comments-div' style='flex: 1; min-width: 0;'>"
div_positive += "<h4>Principais Positivos:</h4>"
div_positive += "<ul class='comments-list'>"

for comentario in df['positive_sentences']:
    div_positive += f"<li>{comentario}</li>"

div_positive += "</ul>"
div_positive += "</div>"

div_negative = "<div class='comments-div' style='flex: 1; min-width: 0;'>"
div_negative += "<h4>Principais Negativos:</h4>"
div_negative += "<ul class='comments-list'>"

for comentario in df['negative_sentences']:
    div_negative += f"<li>{comentario}</li>"

div_negative += "</ul>"
div_negative += "</div>"

div_comentarios = "<div style='display: flex; padding: 10px;'>"
div_comentarios += div_positive
div_comentarios += div_negative
div_comentarios += "</div>"

st.markdown(div_comentarios, unsafe_allow_html=True)