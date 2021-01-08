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
option = st.sidebar.selectbox(
    'Kantons ',
     ['Zürich', 'Zug'])

@st.cache
def read_data():
    impf = pd.read_excel("impfkategorien.xlsx", skiprows=2)
    impf_ = impf.groupby("Priorität").sum()
    impf_plt = pd.DataFrame(impf_["Grösse der Zielgruppe schweizweit laut BAG-Schätzung"]).transpose()
    impf_plt["AnzahlImpfungen"] = 0
    impf_plt = pd.DataFrame(np.array([[0,0,0,0,0,1000000]]), columns=['P1', 'P2', 'P3', 'P4', 'Sonstige', 'AnzahlImpfungen']).append(impf_plt, ignore_index=True)
    data = impf_plt.rename(index={0: "Anzahl Impfungen",1: "Anzahl Personen"})
    return data

data = read_data()

import datetime
today = st.date_input("Today is", datetime.datetime.now())

agree = st.checkbox("Show data")
if agree:
    st.table(data)


st.markdown("Anzahl Impfungen im Vergleich zu Anzahl Personen")
pal = sns.color_palette("BuGn")
mio = ["0 Mio.", "1 Mio.", "2 Mio.", "3 Mio.", "4 Mio.", "5 Mio.", "6 Mio.", "7 Mio."]
ax = data.plot(kind='barh', stacked=True, color= pal)
ax.set_xticklabels(mio)
st.pyplot()

