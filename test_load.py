import requests
from datetime import datetime, timedelta

url = "http://localhost:8000/products/fbv/100/"


def request_products():
    response = requests.get(url)



total_requests = []

for i in range(10):
    time_before = datetime.now()
    request_products()
    time_after = datetime.now()
    elapsed_time = time_after - time_before
    total_requests.append(elapsed_time)
    print(f"Request {i + 1}: {int(elapsed_time.total_seconds() * 1000)} ms")

print(f"Average response time: {int(sum(total_requests, timedelta(0)).total_seconds() * 1000 / len(total_requests))} ms")