import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt
import requests
import s3fs
import os

data = pd.read_csv("df_undersample.csv")

if st.checkbox("Dataframe complet"):
    st.dataframe(data)

ID_client = st.number_input("Numéro client: ", step=1)

max_days_graph = sns.displot(data["PREV_DAYS_DECISION_MAX"])


st.pyplot(max_days_graph)