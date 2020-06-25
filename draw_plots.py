import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

def load_data(state="al"):
    data_url = "https://covidtracking.com/api/v1/states/" + state + "/daily.json"
    state_df = pd.read_json(data_url)
    return state_df

def process_state_tracker(df):
    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df.sort_values(by=["date"], inplace=True)
    df["hosp_7day"] = df.hospitalizedCurrently.rolling(7).mean()
    df["pct_pos"] = df.positiveIncrease / df.totalTestResultsIncrease
    df["death_7day"] = df.deathIncrease.rolling(7).mean()
    
def create_plot(data, state_data, col, col_dict, state="al"):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data[col_dict[col]].rolling(7).mean(),
            name="7-day average",
            marker_color="crimson"
        ))

    fig.add_trace(
        go.Bar(
            x=data["date"],
            y=data[col_dict[col]],
            name=col,
            marker_color="rgba(52, 152, 219, 0.8)"
        ))

    if state_data[state]["Phase 1 Date"] != "":
        fig.add_trace(
            go.Scatter(
                x=[pd.to_datetime(state_data[state]["Phase 1 Date"]), pd.to_datetime(state_data[state]["Phase 1 Date"])],
                y=[0, data[col_dict[col]].max()*.98],
                showlegend=True,
                name="Phase 1 Date",
                mode="lines",
                hovertemplate="Phase 1: %{x}<extra></extra>",
                opacity=0.8,
                line=dict(
                    color='#00897B',
                    width=2,
                    dash="dash"
                    )
            ))

    if state_data[state]["Phase 2 Date"] != "":
        fig.add_trace(
            go.Scatter(
                x=[pd.to_datetime(state_data[state]["Phase 2 Date"]), pd.to_datetime(state_data[state]["Phase 2 Date"])],
                y=[0, data[col_dict[col]].max()*.98],
                showlegend=True,
                name="Phase 2 Date",
                mode="lines",
                hovertemplate="Phase 2: %{x}<extra></extra>",
                opacity=0.8,
                line=dict(
                    color='#7CB342',
                    width=2,
                    dash="dash"
                    )
            ))
        
    if state_data[state]["Phase 3 Date"] != "":
        fig.add_trace(
            go.Scatter(
                x=[pd.to_datetime(state_data[state]["Phase 3 Date"]), pd.to_datetime(state_data[state]["Phase 3 Date"])],
                y=[0, data[col_dict[col]].max()*.98],
                showlegend=True,
                name="Phase 3 Date",
                mode="lines",
                hovertemplate="Phase 3: %{x}<extra></extra>",
                opacity=0.8,
                line=dict(
                    color='#FDD835',
                    width=2,
                    dash="dash"
                    )
            ))

    fig.update_layout(
        title=col,
        yaxis=dict(range=[0,data[col_dict[col]].max()*1.02]),
        xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1mo",
                     step="month",
                     stepmode="backward"),
                dict(count=14,
                     label="2wk",
                     step="day",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ))

    return st.plotly_chart(fig, use_container_width=True)

def tests_plot(data):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(
        go.Bar(
            x=data["date"],
            y=data["totalTestResultsIncrease"],
            name="Tests Completed",
            marker_color="rgba(52, 152, 219, 0.8)"
        ))

    fig.add_trace(
        go.Scatter(
            x=data["date"],
            y=data["pct_pos"].rolling(7).mean()*100, 
            name="Percent Positive",
            line=dict(
                color='firebrick', 
                width=2,
                dash='dot'
            )
        ),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Testing Data",
        xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1mo",
                     step="month",
                     stepmode="backward"),
                dict(count=14,
                     label="2wk",
                     step="day",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
    )

    # Set y-axes titles
    fig.update_yaxes(
        title_text="Tests Completed",
        range=[0,data["totalTestResultsIncrease"].max()*1.02],
        secondary_y=False
    )
    fig.update_yaxes(
        title_text="Percent Positive", 
        range=[0,100], 
        dtick=10, 
        secondary_y=True,
    )

    return st.plotly_chart(fig)
