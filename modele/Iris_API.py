from flask import Flask, request, jsonify
import joblib
import numpy as np
import json


knn = joblib.load('modele/iris_knn.pkl')
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    # obtenir les données de la requête
    data = request.get_json(force=True)

    # effectuer la prédiction
    prediction = knn.predict(data)

    # préparer la réponse
    prediction_list = json.dumps(prediction.tolist())
    response = {'prediction': prediction_list}

    print(response)
    return jsonify(response)


if __name__ == '__main__':

    app.run(port=8080, debug=False)
