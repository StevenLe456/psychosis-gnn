from datetime import datetime, timedelta
import json
import math
import pickle
import requests
import time

# Functio  to make requests to pushshift api
def make_request(uri, max_retries=5):
    def fire_away(uri):
        response = requests.get(uri)
        assert response.status_code == 200
        return json.loads(response.content)
    current_tries = 1
    while current_tries < max_retries:
        try:
            time.sleep(1)
            response = fire_away(uri)
            return response
        except:
            time.sleep(1)
            current_tries += 1
    return fire_away(uri)


authors = []

url = "https://api.pushshift.io/reddit/submission/search/?size=500&after={}&before={}"

# Containerized main function
def main():
    for t in range(0, 200, 50):
        after = math.floor((datetime.utcnow() - timedelta(days=int(t + 50))).timestamp())
        before = math.floor((datetime.utcnow() - timedelta(days=int(t))).timestamp())
        json_data = make_request(url.format(after, before))
        for data in json_data["data"]:
            authors.append(data["author"])

    with open("./logs/random_author_scraper_log.txt", "w") as l:
        l.write("Number of authors: " + str(len(authors)) + "\n")
        l.write("-----------------------------------------------------\n")
        for a in authors:
            l.write(a + "\n")

    with open("./data/raw/random_authors.pickle", "wb") as p:
        pickle.dump(authors, p)