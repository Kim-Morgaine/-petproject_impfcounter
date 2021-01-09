import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from dataclasses import dataclass
from typing import *
from dataclasses import dataclass

st.title("Vaccination covid 19 counter for switzerland") 

st.sidebar.title("Lookup your Kanton")
st.sidebar.markdown('Interact with the data here')


@st.cache
def read_data():
    impf = pd.read_excel("impfkategorien.xlsx", skiprows=2)
    return impf

data_ = read_data()

impf_ = data_.groupby("Priorität").sum()
impf_plt = pd.DataFrame(impf_["Grösse der Zielgruppe schweizweit laut BAG-Schätzung"]).transpose()
impf_plt["AnzahlImpfungen"] = 0
impf_plt = pd.DataFrame(np.array([[0,0,0,0,0,1000000]]), columns=['P1', 'P2', 'P3', 'P4', 'Sonstige', 'AnzahlImpfungen']).append(impf_plt, ignore_index=True)
data = impf_plt.rename(index={0: "Anzahl Impfungen",1: "Anzahl Personen"})

import datetime
today = st.date_input("Today is", datetime.datetime.now())

agree = st.checkbox("Show data")
if agree:
    st.table(data)

st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown("Anzahl Impfungen im Vergleich zu Anzahl Personen")
pal = sns.color_palette("BuGn")
mio = ["0 Mio.", "1 Mio.", "2 Mio.", "3 Mio.", "4 Mio.", "5 Mio.", "6 Mio.", "7 Mio."]
ax = data.plot(kind='barh', stacked=True, color= pal)
ax.set_xticklabels(mio)
st.pyplot()



st.markdown('Distribution of the risk patients')
df = impf_.drop(columns= ["Grösse der Zielgruppe schweizweit laut BAG-Schätzung"])
bars =('P1', 'P2', 'P3', 'P4', 'Sonstige')
y_pos = np.arange(len(bars))
plt.bar(y_pos,list(df["Bern"]/df["Bern"].sum()))
plt.xticks(y_pos, bars)
st.pyplot()

option = st.sidebar.selectbox(
    'Priority Groups',
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

