curl -X POST -H "Content-Type: application/json" --data @payload.json http://localhost:8000/predict


curl -X POST -H "Content-Type: application/json" --data {"data" : [3.2, 3.0 , 1.6, 0.4]} http://localhost:8000/predict