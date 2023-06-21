import pandas as pd
import streamlit as st
import altair as alt
import ast

# TO DO
# Make get_sentiment_chart have a tooltip display for each individual value
# Create total sentiment means plot

# Page configs
st.set_page_config(
    page_title='Dash Board',
    page_icon='⚙️',
)

# Gets csv file, only supports "games_sentiment" atm
def get_data():
    df = pd.read_csv('data/games_sentiment.csv')
    return df

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

    # Get the mean of all positive values and group them by year
    positive_mean = df[df['classifications_sum'] > 0].groupby(df['time'].dt.year)['classifications_sum'].mean().reset_index()
    # Create chart based on positive_mean
    positive_chart = alt.Chart(positive_mean).mark_line(color='green').encode(
        x=alt.X('time:O', title='Ano'),
        y=alt.Y('classifications_sum:Q', title='Pontuação', axis = alt.Axis(format='~s', )),
    )

    # Get the mean of all negative values and group them by year
    negative_mean = df[df['classifications_sum'] < 0].groupby(df['time'].dt.year)['classifications_sum'].mean().reset_index()
    # Create chart based on negative_mean
    negative_chart = alt.Chart(negative_mean).mark_line(color='red').encode(
        x=alt.X('time:O'),
        y=alt.Y('classifications_sum:Q')
    )
    
    # Defining parameters for the mouse hover function
    hover = alt.selection_point(
        on='mouseover',
        fields=['classifications_sum'],
        nearest=True
    )

    positive_points = positive_chart.transform_filter(hover).mark_circle(size=65)

    # Defining parameters for the tooltips used on the mouse hover function
    positive_tooltips = (
        alt.Chart(positive_mean)
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


data = get_data()
scores_chart = get_scores_chart(data)

# Wizardry to make font size bigger, can't do it elsewhere or streamlit will get angry
scores_chart = scores_chart.configure_axisX(
        labelAngle=0,
        titleFontSize=18
    )
scores_chart = scores_chart.configure_axisY(
        titleFontSize=18
    )

# Page title
st.title('Dashboard')

st.write("Média das pontuações:")
# Plotting the score time series
st.altair_chart(scores_chart.interactive(), use_container_width=True)

sentiment_chart = get_sentiment_chart(data)

# SSDD
sentimen_chart = sentiment_chart.configure_axisX(
        labelAngle=0,
        titleFontSize=18
    )
sentiment_chart = sentiment_chart.configure_axisY(
        titleFontSize=18
    )

st.write("Média dos sentimentos:")
st.altair_chart(sentiment_chart, use_container_width=True)
