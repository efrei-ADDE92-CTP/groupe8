from flask import Flask, request, jsonify
import joblib
import numpy as np
import json
import prometheus_client
from prometheus_client import Counter, Histogram
import time
import re

predict_counter = Counter(
    'predict_requests', 'Number of requests to the predict endpoint')
predict_duration = Histogram(
    'predict_duration_seconds', 'Time taken to handle a predict request', ['method'])

with open('src/modele/iris_knn.pkl', 'rb') as file:
    knn = joblib.load(file)
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    request_start = time.time()

    # obtenir les données de la requête
    data = request.get_json(force=True)

    # effectuer la prédiction
    prediction = knn.predict(data)

    # labels
    iris_labels = ['iris setosa', 'iris versicolor', 'iris virginica']

    # préparer la réponse
    prediction_list = json.dumps(prediction.tolist())
    iris_predicted = iris_labels[prediction[0]]
    response = {'prediction': iris_predicted}

    # incrémente le compteur
    predict_counter.inc()
    # obtenir la durée de la requête
    predict_duration.labels(iris_predicted).observe(
        time.time() - request_start)

    print(response)
    return jsonify(response)


@app.route('/metrics', methods=['GET'])
def get_counter():
    response = prometheus_client.generate_latest(
        predict_counter).decode("utf-8")
    return jsonify(response)


@app.route('/metrics/duration', methods=['GET'])
def get_duration():
    response = prometheus_client.generate_latest(
        predict_duration).decode("utf-8")
    return jsonify(response)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=False)
