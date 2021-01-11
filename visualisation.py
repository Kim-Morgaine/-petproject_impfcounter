import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import altair as alt
from dataclasses import dataclass
import geopandas as gpd

st.title("COVID-19 Vaccine Dashboard") 
st.write("| A dashboard for the ongoing process of vaccinations in Switzerland")
st.write("The world is in the midst of a COVID-19 pandemic. Vaccines save millions of lives each year. Vaccines work by training and preparing the body’s natural defences, the immune system, to recognize and fight off the viruses and bacteria they target. There are currently more than 50 COVID-19 vaccine candidates in trials. This dashboard is an approach to visualise the vaccination progress in Switzerland.")
import datetime
today = st.date_input("Today is", datetime.datetime.now())


st.sidebar.title("Visualization Selector")
st.sidebar.write("Select accordingly:")

@st.cache
def read_data():
    impf = pd.read_excel("impfkategorien.xlsx", skiprows=2)
    return impf
@st.cache
def read_dummy():
    df = pd.read_excel("dummy_data.xlsx")
    return df

@st.cache
def info_dummy():
    df = pd.read_excel("mapdata_dummy.xlsx")
    return df

@st.cache
def map_dummy():
    df = gpd.read_file('data/CHE_adm1.shp')
    return df



#Read Data
data_ = read_data()

#Show data
agree = st.checkbox("Show data")
if agree:
    st.subheader("Vaccination Data")
    st.write(data_)

#Prepare Data
impf_ = data_.groupby("Priorität").sum()
d1 =impf_[["Grösse der Zielgruppe schweizweit laut BAG-Schätzung"]]
d1 = d1.rename(columns={"Priorität": "Priority","Grösse der Zielgruppe schweizweit laut BAG-Schätzung":"Vaccinations"}).reset_index()
d1["Site"] = list(np.repeat("Anzahl Personen", 5))
d1 = d1.rename(columns={"Priorität": "Priority"})
d2 = pd.DataFrame({'Priority': ["P1","P2","P3","P4","Sonstige"], 'Vaccinations': [0,0,0,0,1000000], "Site" : list(np.repeat("Anzahl Impfungen", 5))})
df3 = pd.concat([d1, d2])

#Stack barplot
st.header("Current state of amount of vaccinations and priority groups")
stack = alt.Chart(df3).mark_bar(size = 70).encode(
    alt.X('sum(Vaccinations):Q', axis=alt.Axis(title="")),
    alt.Y('Site:N', axis=alt.Axis(title="")),
    color=alt.Color('Priority', scale=alt.Scale(scheme='pastel1'),legend=alt.Legend(title="Priority Groups"))
).properties(
    width=800,
    height=500).configure_axis(
    labelFontSize=17,
    titleFontSize=20)
st.altair_chart(stack)

st.subheader("Select the box to see the criteria for the priority groups")
agree = st.checkbox("Show Description")
if agree:
    option = st.selectbox(
        "Description of the Priority Groups",
        ['P1', 'P2', 'P3', 'P4', 'Sonstige'])

    if option == "P1":
        st.table(data_["Beschreibung"].loc[data_['Priorität'] == "P1"])
    if option == "P2":
        st.table(data_["Beschreibung"].loc[data_['Priorität'] == "P2"])
    if option == "P3":
        st.table(data_["Beschreibung"].loc[data_['Priorität'] == "P3"])
    if option == "P4":
        st.table(data_["Beschreibung"].loc[data_['Priorität'] == "P4"])
    if option == "Sonstige":
        st.table(data_["Beschreibung"].loc[data_['Priorität'] == "Sonstige"])

## Barchart
st.header('Distribution in percentage of the different Vaccination groups')
df1 = impf_.reset_index()
df1['Schwitzerland'] = df1["Bern"]/df1["Bern"].sum()
bars = alt.Chart(df1).mark_bar(size = 80).encode(
    x='Priorität',
    y='Schwitzerland').configure_mark(
    color='#ffbb78').properties(
    width=800,
    height=500).configure_axis(
    labelFontSize=17,
    titleFontSize=20)
st.altair_chart(bars)


df_dummy = read_dummy()
manufacturer_input = st.multiselect(
'Manufacturer',df_dummy.groupby("manufacturer").count().reset_index()["manufacturer"].tolist())
if len(manufacturer_input) > 0:
    df_dummy = df_dummy[df_dummy["manufacturer"].isin(manufacturer_input)]
shipping_volume = alt.Chart(df_dummy).transform_filter(
   alt.datum.shipping_volume_cumulated > 0  
).mark_line().encode(
    x=alt.X('shipping_date', type='nominal', title='Date'),
    y=alt.Y('sum(shipping_volume_cumulated):Q',  title='Shipping Volume'),
    color='manufacturer',
    tooltip = 'sum(shipping_volume_cumulated)',
).properties(
    width=800,
    height=600
).configure_axis(
    labelFontSize=17,
    titleFontSize=20
)

#Time Chart
st.header('Comulated Shipping Value Over Time')
st.altair_chart(shipping_volume)

#Switzerland Map
map_df = map_dummy()
info_dummy = info_dummy()

merge=pd.merge(map_df,info_dummy,on='NAME_1')

st.header('Distribution of P1 in the Kantons')
st.set_option('deprecation.showPyplotGlobalUse', False)
swiss_map = merge.plot(column='P1', scheme="quantiles",
           figsize=(25, 20),
           legend=True,cmap='coolwarm')
st.pyplot()
