import streamlit as st
import pandas as pd

df = pd.read_csv("C:\\Users\\User\\OneDrive\\Github\\AIpp\\AIpp\\data\\games_sentiment.csv")
df.sort_values('likes', inplace=True, ascending=False)
df = df.head()
df = df.reset_index(drop=True)

positive = df['positive_sentences']
negative = df['negative_sentences']

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

# Exibição dos comentários
div_positive = "<div class='comments-div'>"
div_positive += "<h4>Positivos:</h4>"
div_positive += "<ul class='comments-list'>"
for comentario in df['positive_sentences']:
    div_positive += f"<li>{comentario}</li>"
div_positive += "</ul>"
div_positive += "</div>"

div_negative = "<div class='comments-div'>"
div_negative += "<h4>Negativos:</h4>"
div_negative += "<ul class='comments-list'>"
for comentario in df['negative_sentences']:
    div_negative += f"<li>{comentario}</li>"
div_negative += "</ul>"
div_negative += "</div>"


div_comentarios = "<div style=' flex: 1; display: flex; flex-direction: row; background-color: #f5f5f5; padding: 10px;'>"
#div_comentarios += "<h3>Principais Comentários</h3>"
#div_comentarios += f"<p>{[x for x in positive]}</p>"
div_comentarios += div_positive
div_comentarios += div_negative
div_comentarios += "</div>"

st.markdown(div_comentarios, unsafe_allow_html=True)


