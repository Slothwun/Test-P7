import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import s3fs
import os

st.title("Prédiction de solvabilité client")

data = pd.read_csv("df_final.csv")

if st.checkbox("Dataframe complet"):
    st.dataframe(data)

ID_client = st.number_input("Numéro client: ", step=1)

response = requests.get("http://127.0.0.1:5000/test", params={"id":ID_client})

jsonResponse = response.json()
"ID client: ", jsonResponse["id_client"]
"Prédiction: ", jsonResponse["prediction"]

solvabilité_client = jsonResponse["prediction"]
def message_client(predi):
    if predi == 1.0 :
        return"Le client n'est pas solvable."
    else: return"Le client est solvable."

st.write(message_client(solvabilité_client))

st.header("Probabilités du client : ")
"Pourcentage solvable (0) :", round(jsonResponse["probability"][0][0] *100, 2)
"Pourcentage non solvable (1) :", round(jsonResponse["probability"][0][1] *100, 2)

st.header("Variables qui influencent le plus la prédiction du client :")

"- Variable 1 :", jsonResponse["tableau lime"][0][0]
"Valeur de la variable 1 =", round(jsonResponse["tableau lime"][0][1], 3)

"- Variable 2 :", jsonResponse["tableau lime"][1][0]
"Valeur de la variable 2 =", round(jsonResponse["tableau lime"][1][1], 3)

"- Variable 3 :", jsonResponse["tableau lime"][2][0]
"Valeur de la variable 3 =", round(jsonResponse["tableau lime"][2][1], 3)


st.header("Variables les plus importantes pour le modèle:")

valeurs_client = data[data["SK_ID_CURR"] == ID_client]


"- Prix moyen du dernier achat :"
fig1 = px.histogram(data, x="PREV_AMT_GOODS_PRICE_MEAN", labels={"PREV_AMT_GOODS_PRICE_MEAN":"Prix moyen du dernier achat"})
fig1.update_yaxes(title=" Nombre de clients")
st.plotly_chart(fig1)
"Prix moyen du dernier achat du client : ", valeurs_client["PREV_AMT_GOODS_PRICE_MEAN"]


car_counter = data["FLAG_OWN_CAR"].value_counts()
"- Répartition des propriétaires de voitures :"
fig2 = px.bar(data, x=car_counter.index, y=car_counter.values, labels={"x":"Possession de voiture", "y":"Nombre de clients"})
fig2.update_layout(xaxis= dict(tickmode="array", tickvals = [0, 1], ticktext = ("Pas de voiture (0)", "Voiture (1)")))
st.plotly_chart(fig2)
"Voiture du client :", valeurs_client["FLAG_OWN_CAR"]

gender_counter = data["CODE_GENDER"].value_counts()
gender_labels = ["Hommes (1)", "Femmes (0)"]
"- Proportions des genres :"
fig3 = px.pie(data, values=gender_counter.values, names=gender_labels)
st.plotly_chart(fig3)
"Genre du client :", valeurs_client["CODE_GENDER"]
