from flask import Flask, request, jsonify
import joblib
import numpy as np
import json
from prometheus_client import Counter, Histogram
import time

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
    # incrémente le compteur
    predict_counter.inc()

    # obtenir les données de la requête
    data = request.get_json(force=True)

    # effectuer la prédiction
    prediction = knn.predict(data)

    # préparer la réponse
    prediction_list = json.dumps(prediction.tolist())
    response = {'prediction': prediction_list}

    # obtenir la durée de la requête
    predict_duration.labels('post').observe(time.time() - request_start)

    print(response)
    return jsonify(response)


@app.route('/metrics/counter', methods=['GET'])
def get_counter():
    response = {'counter': int(predict_counter._value)}
    return jsonify(response)


@app.route('/metrics/duration', methods=['GET'])
def get_duration():
    response = {'duration': {
        'sum': predict_duration._sum, 'count': predict_duration._count}}
    return jsonify(response)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=False)
