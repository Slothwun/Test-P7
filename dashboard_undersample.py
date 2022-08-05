import streamlit as st
import pandas as pd
import numpy as np
import requests

st.title("Essai de dashboard pour undersample")

data = pd.read_csv("df_undersample.csv")

if st.checkbox("Dataframe complet"):
    st.dataframe(data)

ID_client = st.number_input("Numéro client: ", step=1)

"Numéro client: ", ID_client
response = requests.get("http://127.0.0.1:5000/test", params={"id":ID_client})

jsonResponse = response.json()
"ID client: ", jsonResponse["id_client"]
"Prediction: ", jsonResponse["prediction"]

if st.checkbox("Infos client: "):
    data[data["SK_ID_CURR"] == ID_client]

st.bar_chart(data["CODE_GENDER"])