curl --location --request POST 'http://localhost:8080/predict' \
--header 'Content-Type: application/json' \
--data-raw '[[3.2, 5.7, 2.1, 7.9]]'

curl --location --request GET 'http://localhost:8080/metrics/counter'

curl --location --request GET 'http://localhost:8080/metrics/duration'

docker build --tag iris_project -f Dockerfile .

sudo docker run -p 8080:8080 iris_project

