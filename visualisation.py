import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import altair as alt
from dataclasses import dataclass

st.title("Vaccination covid 19 counter for switzerland") 

#st.sidebar.title("Lookup your Kanton")
#st.sidebar.markdown('Interact with the data here')


@st.cache
def read_data():
    impf = pd.read_excel("impfkategorien.xlsx", skiprows=2)
    return impf

def read_dummy():
    df = pd.read_excel("dummy_data.xlsx")
    return df

data_ = read_data()

impf_ = data_.groupby("Priorität").sum()
d1 =impf_[["Grösse der Zielgruppe schweizweit laut BAG-Schätzung"]]
d1 = d1.rename(columns={"Priorität": "Priority","Grösse der Zielgruppe schweizweit laut BAG-Schätzung":"Vaccinations"}).reset_index()
d1["Site"] = list(np.repeat("Anzahl Personen", 5))
d1 = d1.rename(columns={"Priorität": "Priority"})
d2 = pd.DataFrame({'Priority': ["P1","P2","P3","P4","Sonstige"], 'Vaccinations': [0,0,0,0,1000000], "Site" : list(np.repeat("Anzahl Impfungen", 5))})
df3 = pd.concat([d1, d2])
#impf_plt = pd.DataFrame(impf_["Grösse der Zielgruppe schweizweit laut BAG-Schätzung"]).transpose()
#impf_plt["AnzahlImpfungen"] = 0
#impf_plt = pd.DataFrame(np.array([[0,0,0,0,0,1000000]]), columns=['P1', 'P2', 'P3', 'P4', 'Sonstige', 'AnzahlImpfungen']).append(impf_plt, ignore_index=True)
#data = impf_plt.rename(index={0: "Anzahl Impfungen",1: "Anzahl Personen"})

import datetime
today = st.date_input("Today is", datetime.datetime.now())

agree = st.checkbox("Show data")
if agree:
    st.subheader("Vaccination Data")
    st.write(data_)
    #st.table(data)

#st.set_option('deprecation.showPyplotGlobalUse', False)
#st.markdown("Anzahl Impfungen im Vergleich zu Anzahl Personen")
#pal = sns.color_palette("BuGn")
#mio = ["0 Mio.", "1 Mio.", "2 Mio.", "3 Mio.", "4 Mio.", "5 Mio.", "6 Mio.", "7 Mio."]
#ax = data.plot(kind='barh', stacked=True, color= pal)
#ax.set_xticklabels(mio)
#st.pyplot()

st.markdown("Anzahl Impfungen im Vergleich zu Anzahl Personen")
stack = alt.Chart(df3).mark_bar().encode(
    x='sum(Vaccinations):Q',
    y='Site:N',
    color='Priority'
).properties(width=800, height=500)
st.altair_chart(stack)


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

st.markdown('Distribution in percentage of the different Vaccination groups')
df = impf_.drop(columns= ["Grösse der Zielgruppe schweizweit laut BAG-Schätzung"])
df = df.rename(columns={"Zürich": "Switzerland"})
st.bar_chart(df["Switzerland"]/df["Switzerland"].sum())

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
    width=1500,
    height=600
).configure_axis(
    labelFontSize=17,
    titleFontSize=20
).properties(width=800, height=600)

st.subheader('Comulated Shipping Value Over Time')
st.altair_chart(shipping_volume)

