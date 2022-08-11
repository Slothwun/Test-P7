import streamlit as st
import pandas as pd
import numpy as np
import requests
import s3fs
import os

fs = s3fs.S3FileSystem(anon=False)

st.title("Essai de dashboard pour undersample")

def read_file(filename):
    with fs.open(filename) as f:
        return f.read().decode("utf-8")

data = read_file("testbucketpourp7/df_undersample.csv")

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