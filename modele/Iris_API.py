from flask import Flask, request, jsonify
import joblib


knn = joblib.load('iris_knn.pkl')
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # obtenir les données de la requête
    data = request.get_json(force=True)

    # effectuer la prédiction
    prediction = knn.predict(data)

    # préparer la réponse
    response = {'prediction': prediction}
    return jsonify(response)

if __name__ == '__main__':

    app.run(port=8000, debug=True)



     
 
