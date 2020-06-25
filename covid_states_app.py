import streamlit as st
import numpy as np
from draw_plots import tests_plot, load_data, process_state_tracker, create_plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import timedelta


#@st.cache(allow_output_mutation=True)
hosp_col_dict = {
    "Hospital Census":"hospitalizedCurrently",
    "New Hospitalizations":"hospitalizedIncrease"
}
other_col_dict = {
    "New COVID Cases": "positiveIncrease",
    "COVID-related Deaths": "deathIncrease"
}

# get state info 
with open('state_data.json') as json_file: 
    state_data = json.load(json_file) 

    
## SIDEBAR
state = st.sidebar.selectbox(
    "Which State Would You Like to view?",
    [k for k,v in state_data.items()]
)
site_title = st.title(state+' COVID Trends Data')

hosp_col = st.sidebar.selectbox(
    'Do you want New Hospitalizations or Census?',
     [k for k,v in hosp_col_dict.items()])
st.sidebar.markdown("---")


## MAIN SECTION
# load and process the data
data = load_data(state=state_data[state]["abbr"])
process_state_tracker(data)

# deaths count
total_deaths = int(data["death"].iloc[-1])
rel_deaths = np.round(data["death"].iloc[-1] / (state_data[state]["Population"] / 100000), 1)
st.sidebar.markdown(
    '<p style="font-size:120%;font-weigth;bold;color:#444444; text-align: center;">Total COVID-related Deaths<br /><span style="font-size:300%;font-family: Impact, Charcoal, sans-serif;">'+str(total_deaths)+'</span><br /><span style="font-size:90%;">'+str(rel_deaths)+' per 100,000</span></p>',
    unsafe_allow_html=True
)

# percent positive: 7-day average
pct_pos = np.round(data["pct_pos"].iloc[-7:].mean()*100, 1)
if pct_pos > 10:
    color = 'red'
elif pct_pos > 5 and pct_pos <=10:
    color = 'orange'
else:
    color = '#444444'
st.sidebar.markdown("---")

if pct_pos > 100:
    st.sidebar.markdown(
        '<p style="font-size:120%;font-weigth;bold;color:#444444; text-align: center;">Percent Positve (Past Week)<br /><span style="font-size:300%;font-family: Impact, Charcoal, sans-serif;">No Data</span></p>',
        unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        '<p style="font-size:120%;font-weigth;bold;color:#444444; text-align: center;">Percent Positve (Past Week)<br /><span style="font-size:300%;font-family: Impact, Charcoal, sans-serif;color:'+color+';">'+str(pct_pos)+'%</span></p>',
        unsafe_allow_html=True
    )

## INTRO
st.write(
    "The purpose of this app is to be able to view multiple COVID-related metrics to get a more holistic view of trends in each state."
)
phases = st.checkbox("Show reopening dates and measures")

if phases:
    with open(state_data[state]["Policy"], 'r') as reader:
        st.markdown(reader.read())

# COVID+ hospitalizations
create_plot(
    data, 
    state_data, 
    col=hosp_col, 
    col_dict=hosp_col_dict, 
    state=state
)

# New COVID Cases
create_plot(
    data, 
    state_data, 
    col="New COVID Cases", 
    col_dict=other_col_dict, 
    state=state
)

# COVID testing plot
tests_plot(data=data)

# COVID-related deaths plot
create_plot(
    data, 
    state_data, 
    col="COVID-related Deaths", 
    col_dict=other_col_dict, 
    state=state
)

# Federal Phase Definitions
guidelines = st.checkbox("Show Federal Guideline Definitions")

if guidelines:
    with open('guidelines.md', 'r') as reader:
        st.markdown(reader.read())