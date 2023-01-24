FROM python:3.8.13

RUN apt update
RUN apt install python3

# set the working directory in the container
WORKDIR /src

COPY src/modele/iris_api.py ./src/modele/

# copy the dependencies file to the working directory
COPY requirements.txt .

RUN mkdir -p src/modele

COPY . .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# command to run on container start
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "python3", "./src/modele/iris_api.py" ]
