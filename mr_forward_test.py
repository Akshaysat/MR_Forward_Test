import json
import numpy as np
import pandas as pd
import requests
import streamlit as st
import plotly.express as px

api_url_mr = "https://e91pez1xi8.execute-api.ap-south-1.amazonaws.com/pnl?"
payload = {}
headers= {}
response_mr = requests.request("GET", api_url_mr, headers=headers, data = payload)
data = json.loads(response_mr.text)['data']

df = pd.DataFrame(data)
df = df.rename(columns = {'_id':'Date'})
#df = df.set_index('_id')
df = df.iloc[::-1]
df['pnl'] = round(df['pnl'],1)
df['cum_pnl'] = df['pnl'].cumsum()
net_roi = round(df['cum_pnl'].iloc[-1]*100/100000,2)
df['month'] = pd.DatetimeIndex(df['Date']).month 
df['year'] = pd.DatetimeIndex(df['Date']).year
df['month'] = pd.to_datetime(df['month'], format='%m').dt.month_name().str.slice(stop=3)
df['month_year'] = (df['month'] + df['year'].astype(str)).str.slice(stop = 7)

df1 = df.groupby(['month_year'],sort = False).sum()
df1['% Returns'] = round(df1['pnl']*100/100000,2)
df1 = df1.reset_index()

fig = px.line(df, x='Date', y='cum_pnl',width = 1000,height = 600)

#Reverse the dataframe
if df.Date[0]:
    df = df[1:]

#st.beta_set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: black;'>Forward Test of Mean Reversion Strategy</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: left; color: black;'>(Capital used is 1 lac with 1x margin)</h3>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: left; color: black;'>PNL Curve</h2>", unsafe_allow_html=True)

st.plotly_chart(fig)
st.title('Net ROI: '+ str(net_roi) + '%')

st.markdown("<h2 style='text-align: left; color: black;'>Date Wise PNL</h2>", unsafe_allow_html=True)
st.table(df[['Date','pnl']].astype('object'))

st.markdown("<h2 style='text-align: left; color: black;'>Month Wise % Returns</h2>", unsafe_allow_html=True)
st.table(df1[['month_year','% Returns']])
