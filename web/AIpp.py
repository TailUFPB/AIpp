import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import altair as alt
import ast

def score_plot(scores):
    plt.clf()
    colors = ['#228B22', '#00FF7F', '#FFD700', '#FF0000', '#8B0000']
    plt.pie(scores.tolist(), colors=colors, startangle=90, counterclock=False)
    
    plt.size = (5, 5)
    my_circle = plt.Circle((0, 0), 0.75, color='#101414')
    plt.title('Score', y=-0.07, fontsize=18, color='white')

    avg = (scores[1] + 2*scores[2] + 3*scores[3] + 4*scores[4] + 5*scores[5]) / sum(scores.values.tolist())

    plt.text(0, 0, f'{avg:.2f}',
            fontsize=24, ha='center', va='center', color='white')
    
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    return p

def count_pos_reviews_sentiment(reviews_sen):
    count = 0
    for sen in reviews_sen:
        if sen == 1:
            count += 1
    
    return count

def count_neg_reviews_sentiment(reviews_sen):
    count = 0
    for sen in reviews_sen:
        if sen == -1:
            count += 1
    
    return count

def reviews_plot(df):
    colors = ['#00cf0a', '#a80202']

    count_pos = df.apply(count_pos_reviews_sentiment).sum()
    count_neg = df.apply(count_neg_reviews_sentiment).sum()

    plt.pie([count_pos, count_neg], colors=colors, startangle=90, counterclock=False)
    
    plt.size = (5, 5)
    my_circle = plt.Circle((0, 0), 0.75, color='#101414')
    plt.title('Reviews', y=-0.07, fontsize=18, color='white')
    
    percentage = (count_pos/(count_pos+count_neg)) * 100

    plt.text(0, 0, f'{percentage:.2f}%',
            fontsize=22, ha='center', va='center', color='white')
    
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    return p

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

    .tags-list {
        list-style-type: disc;
        margin-left: 20px;
        padding-left: 10px;
    }
</style>
""", unsafe_allow_html=True)

option = st.selectbox(
    'Qual App você deseja analisar?',
    df['app_name'].value_counts().index.tolist()
)

df = df[df['app_name'] == option]
app_tags = app_tags[[option, 'sentiment']] #Dataframe com as tags positivas e negativas dos apps

col1, col2 = st.columns(2)

classifications = df['classifications'].apply(lambda x: ast.literal_eval(x))
reviews_fig = reviews_plot(classifications)
col1.pyplot(reviews_fig, transparent=True)

fig = score_plot(df['score'].value_counts())
col2.pyplot(fig, transparent=True)

div_positive_tags = "<div class='tags-div' style='flex: 1; min-width: 0;'>"
div_positive_tags += "<h4>Características Positivas:</h4>"
div_positive_tags += "<ul class='tags-list'>"

app_pos_tags = app_tags.loc[app_tags['sentiment'] == 1][option] #Separa as tags positivas
app_pos_tags = list(app_pos_tags.values)

for item in app_pos_tags:
    item = eval(item)
    div_positive_tags += f"<li>{item[0].capitalize()}</li>"

div_positive_tags += "</ul>"
div_positive_tags += "</div>"

div_negative_tags = "<div class='tags-div' style='flex: 1; min-width: 0;'>"
div_negative_tags += "<h4>Características Negativas:</h4>"
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

# DO NOT ALTER df_chart. This is the df that's going to be passed to all chart functions
df_chart = df

df = df.head(10)
positive = df['positive_sentences'].apply(lambda x: x[1:-1].split("',"))
negative = df['negative_sentences'].apply(lambda x: x[1:-1].split("',"))

# Exibição dos comentários
div_positive = "<div class='comments-div' style='flex: 1; min-width: 0;'>"
div_positive += "<h4>Principais Positivos:</h4>"
div_positive += "<ul class='comments-list'>"

for comentario in positive[:5]:
    if comentario[0] != '':
        div_positive += f"<li>{comentario[0]}</li>"
    else:
        comentario = positive.iloc[5]
        div_positive += f"<li>{comentario[0]}</li>"

div_positive += "</ul>"
div_positive += "</div>"

div_negative = "<div class='comments-div' style='flex: 1; min-width: 0;'>"
div_negative += "<h4>Principais Negativos:</h4>"
div_negative += "<ul class='comments-list'>"

for comentario in negative[:5]:
    if comentario[0] != '':
        div_negative += f"<li>{comentario[0]}</li>"
    else:
        comentario = positive.iloc[5]
        div_negative += f"<li>{comentario[0]}</li>"

div_negative += "</ul>"
div_negative += "</div>"

div_comentarios = "<div style='display: flex; padding: 10px;'>"
div_comentarios += div_positive
div_comentarios += div_negative
div_comentarios += "</div>"

st.markdown(div_comentarios, unsafe_allow_html=True)

# ==================================================================
#                              Dashboard
# ==================================================================

def get_time(df):
    # Convert "time" column to datetime type
    df['time'] = pd.to_datetime(df['time'], dayfirst=True)
    return df

# Prepares everything to plot the time series
def get_scores_chart(df):
    df = get_time(df)
    # Group the data by year and calculate the mean value
    mean_df = df.groupby(df['time'].dt.year)['score'].mean().reset_index()

    # Defining parameters for the mouse hover function
    hover = alt.selection_point(
        on='mouseover',
        fields=['score'],
        nearest=True
    )

    # Create the Altair time series plot
    chart = alt.Chart(mean_df).mark_line().encode(
        x=alt.X('time:O', title='Ano'),
        y=alt.Y('score:Q', title='Pontuação', axis = alt.Axis(format='~s', ))
    )

    # Adds the little funny dots to the nearest data point plotted on the graph
    points = chart.transform_filter(hover).mark_circle(size=65)

    # Defining parameters for the tooltips used on the mouse hover function
    tooltips = (
        alt.Chart(mean_df)
        .mark_rule()
        .encode(
            x="time:O",
            y="score:Q",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("time:O", title="Ano"),
                alt.Tooltip("score:O", title="Pontuação"),
            ],
        )
        .add_selection(hover)
    )

    # Combining all features of the plot
    layer_chart = alt.layer(chart, points, tooltips).interactive()
    return layer_chart

# This function makes my head hurt and my knees weak
# In here we calculate the mean of the sentiment values, the ammount of positive values and the ammount of negative values
# After that, the function joins everything in a single graph and returns it
def get_sentiment_chart(df):
    # Converting the "classifications" column value to a literal list
    df['classifications'] = df['classifications'].apply(lambda x: ast.literal_eval(x))
    # Sum all values of "classifications"
    df['classifications_sum'] = df['classifications'].apply(sum)

    # Get the sum of positive values and group them by year
    positive_sum = df[df['classifications_sum'] > 0].groupby(df['time'].dt.year)['classifications_sum'].sum().reset_index()
    # Create chart based on positive_sum
    positive_chart = alt.Chart(positive_sum).mark_line(color='green').encode(
        x=alt.X('time:O', title='Ano'),
        y=alt.Y('classifications_sum:Q', title='Pontuação', axis = alt.Axis(format='~s', )),
    )

    # Get the sum of negative values and group them by year
    negative_sum = df[df['classifications_sum'] < 0].groupby(df['time'].dt.year)['classifications_sum'].sum().reset_index()
    # Create chart based on negative_sum
    negative_chart = alt.Chart(negative_sum).mark_line(color='red').encode(
        x=alt.X('time:O'),
        y=alt.Y('classifications_sum:Q'),
    )
    
    # Defining parameters for the mouse hover function
    hover = alt.selection_multi(
        on='mouseover',
        fields=['classifications_sum'],
        nearest=True
    )

    positive_points = positive_chart.transform_filter(hover).mark_circle(size=65)

    # Defining parameters for the tooltips used on the mouse hover function
    positive_tooltips = (
        alt.Chart(positive_sum)
        .mark_rule()
        .encode(
            x="time:O",
            y="classifications_sum:Q",
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip("time:O", title="Ano"),
                alt.Tooltip("classifications_sum:O", title="Pontuação"),
            ],
        )
        .add_selection(hover)
    )

    # Combining all features of the plot
    layer_chart = alt.layer(negative_chart, positive_tooltips, positive_points, positive_chart).interactive()
    return layer_chart


scores_chart = get_scores_chart(df_chart)

# Wizardry to make font size bigger, can't do it elsewhere or streamlit will get angry
scores_chart = scores_chart.configure_axisX(
        labelAngle=0,
        titleFontSize=18
    )
scores_chart = scores_chart.configure_axisY(
        titleFontSize=18
    )

st.write("Média das pontuações:")
# Plotting the score time series
st.altair_chart(scores_chart.interactive(), use_container_width=True)

sentiment_chart = get_sentiment_chart(df_chart)

# SSDD
sentimen_chart = sentiment_chart.configure_axisX(
        labelAngle=0,
        titleFontSize=18
    )
sentiment_chart = sentiment_chart.configure_axisY(
        titleFontSize=18
    )

st.write("Soma das reviews:")
st.altair_chart(sentiment_chart, use_container_width=True)