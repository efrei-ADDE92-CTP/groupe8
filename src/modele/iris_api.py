from flask import Flask, request, jsonify
import joblib
import numpy as np
import json
from prometheus_client import Counter

predict_counter = Counter('predict_requests', 'Number of requests to the predict endpoint')

with open('src/modele/iris_knn.pkl', 'rb') as file:
    knn = joblib.load(file)
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():

    # incrémente le compteur
    predict_counter.inc()

    # obtenir les données de la requête
    data = request.get_json(force=True)

    # effectuer la prédiction
    prediction = knn.predict(data)

    # préparer la réponse
    prediction_list = json.dumps(prediction.tolist())
    response = {'prediction': prediction_list}

    print(response)
    return jsonify(response)

@app.route('/metrics', methods=['GET'])
def get_counter():
    response = {'counter': predict_counter}
    return jsonify(response)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=False)
