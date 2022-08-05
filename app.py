
from bs4 import ResultSet
import flask
from flask import request, jsonify

app = flask.Flask(__name__)

#@app.route("/")
#def home():
 #   return "Hello, Flask!"


import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn import model_selection
from sklearn.svm import SVC
from lime.lime_tabular import LimeTabularExplainer
from joblib import load



df = pd.read_csv("df_undersample.csv")
df = df.drop(["TARGET"], axis=1)

model = load("modèle_undersample.joblib")

training_set = df.drop(["SK_ID_CURR"], axis=1)

lime_explainer = LimeTabularExplainer(training_data=np.array(training_set), feature_names=training_set.columns,
                    class_names=[0, 1], mode="classification")



@app.route("/test", methods=["GET"])
def ID():
    if "id" in request.args:
        id = int(request.args["id"])
        x, y = prediction_client(df, id)
        results = {"id_client": x, "prediction": y[0]}
        print(results)
        return jsonify(results)
    else:
        return "There's a problem"

def prediction_client(df, id):
    variables = df[df["SK_ID_CURR"] == id]
    variables = variables.drop(["SK_ID_CURR"], axis=1)
    prediction = model.predict(variables)
    print(prediction)

    return id, prediction


app.run()