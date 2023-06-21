import pandas as pd
import streamlit as st
import altair as alt

# TO DO
# Adicionar time series para plotar os positivos e negativos do CSV

# Gets csv file, only supports "games_sentiment" atm
def get_data():
    df = pd.read_csv('data/games_sentiment.csv')
    return df

# Prepares everything to plot the time series
def get_chart(df):
    # Convert "time" column to datetime type
    df['time'] = pd.to_datetime(df['time'], dayfirst=True)

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

data = get_data()
chart = get_chart(data)

# Wizardry to make font size bigger, can't do it elsewhere or streamlit will get angry
chart = chart.configure_axisX(
        labelAngle=0,
        titleFontSize=18
    )
chart = chart.configure_axisY(
        titleFontSize=18
    )

# Page title
st.title('Dashboard')

# Plotting the time series
st.altair_chart(chart.interactive(), use_container_width=True)