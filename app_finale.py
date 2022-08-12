from bs4 import ResultSet
import flask
from flask import request, jsonify

app = flask.Flask(__name__)


import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn import model_selection
from sklearn.svm import SVC
from lime.lime_tabular import LimeTabularExplainer
from joblib import load

df = pd.read_csv("df_undersample.csv")
df = df.drop(["TARGET"], axis=1)

model = load("modèle_final.joblib")

training_set = df.drop(["SK_ID_CURR"], axis=1)

@app.route("/test", methods=["GET"])



def ID():
    if "id" in request.args:
        id_client = int(request.args["id"])
        x, y = prediction_client(df, id_client)
        results = {"id_client": x, "prediction": y[0]}
        return jsonify(results)
    else:
        return "There is a problem"

def prediction_client(df, id_client):
    variables = df[df["SK_ID_CURR"] == id_client]
    variables = variables.drop(["SK_ID_CURR"], axis=1)
    prediction = model.predict(variables)
    print(prediction)

    return id_client, prediction

app.run()