from locust import HttpUser, TaskSet, task, between
import json


class UserTasks(TaskSet):
    headers = {'Content-Type': 'application/json'}
    payload = [[3.2, 5.7, 2.1, 7.9]]

    @task
    def predict(self):
        response = self.client.post(
            "/predict", headers=self.headers, data=json.dumps(self.payload))
        if response.status_code != 200:
            print("Request failed with status code:", response.status_code)


class WebsiteUser(HttpUser):
    tasks = [UserTasks]
    wait_time = between(1, 2)
