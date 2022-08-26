
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



df = pd.read_csv("df_final.csv")
df = df.drop(["TARGET", "Unnamed: 0"], axis=1)

model = load("modèle_final.joblib")



@app.route("/test", methods=["GET"])
def ID():
    if "id" in request.args:
        id = int(request.args["id"])
        x, y, z, w = prediction_client(df, id)
        results = {"id_client": x, "prediction": y[0], "probability": z, "tableau lime": w}
        
        return jsonify(results)
    else:
        return "There's a problem"

def prediction_client(df, id):
    variables = df[df["SK_ID_CURR"] == id]
    index = df[df["SK_ID_CURR"] == id].index
    index = index[0]
    variables = variables.drop(["SK_ID_CURR"], axis=1)

    prediction = model.predict(variables)
    probability = model.predict_proba(variables)
    probability = probability.tolist()
    
    training_set = df.drop(["SK_ID_CURR"], axis=1)
    lime_explainer = LimeTabularExplainer(training_data=np.array(training_set), feature_names=training_set.columns,
                            class_names=[0, 1], mode="classification")
    lime_explanation = lime_explainer.explain_instance(data_row=training_set.iloc[index], predict_fn=model.predict_proba)
    tableau_lime = lime_explanation.as_list()

    return id, prediction, probability, tableau_lime


app.run()