from datetime import datetime, timedelta
import json
import math
import pickle
import requests
import time

# This function makes a request to the pushshift api
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


# Store the user flairs an author of a post must have to identify psychotic authors
user_flairs = ["Psychoses", 
    "Schizophrenia", 
    "Paranoid Schizophrenia", 
    "Catatonic Schizophrenia", 
    "Residual Schizophrenia", 
    "Residual Schizophrenia",
    "Schizoaffective (Bipolar)",
    "Schizoaffective (Depressive)",
    "Schizophreniform"]

# URL to pass to pushshift api
url = "https://api.pushshift.io/reddit/submission/search/?subreddit=schizophrenia&size=500&after={}&before={}"

authors = {}

#Containerize main functionality
def main():
    # Get 500 posts per time frame to maximize data obtained
    for t in range(0, 3000, 50):
        after = math.floor((datetime.utcnow() - timedelta(days=int(t + 50))).timestamp())
        before = math.floor((datetime.utcnow() - timedelta(days=int(t))).timestamp())
        json_data = make_request(url.format(after, before))
        for data in json_data["data"]:
            if data["author_flair_text"] in user_flairs:
                authors[data["author"]] = data["author_flair_text"]

    # Write to log
    log = open("./logs/author_scraper_log.txt", "w")
    log.write("Number of unique authors: " + str(len(authors)) + "\n")
    log.write("-----------------------------------------------------\n")
    flairs = {}
    for author, user_flair in authors.items():
        log.write(author + " " + user_flair + "\n")
        if user_flair not in flairs:
            flairs[user_flair] = 1
        else:
            flairs[user_flair] += 1
    log.write("-----------------------------------------------------\n")
    for k, v in flairs.items():
        log.write(k + " " + str(v) + "\n")
    log.close()

    # Save author information
    with open("./data/raw/authors.pickle", "wb") as p:
        pickle.dump(authors, p)