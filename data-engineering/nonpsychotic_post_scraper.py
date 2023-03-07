import json
import pickle
import requests
import spacy
import statistics
import time


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


nlp = spacy.load("en_core_web_md")

submissions_url = "https://api.pushshift.io/reddit/submission/search/?size=500&author={}&after=365d&before=0d"
comments_url = "https://api.pushshift.io/reddit/comment/search/?size=500&author={}&after=365d&before=0d"

def main():
    posts = {}
    lengths = []
    num_posts = 0
    num_submissions = 0
    num_comments = 0

    with open("./data/random_authors.pickle", "rb") as p:
        authors = pickle.load(p)

    for author in authors:
        l = []
        submissions_data = make_request(submissions_url.format(author))
        comments_data = make_request(comments_url.format(author))
        for submission in submissions_data["data"]:
            if "selftext" in submission.keys():
                doc = nlp(submission["selftext"])
                if len(doc) >= 100:
                    num_posts += 1
                    num_submissions += 1
                    lengths.append(len(doc))
                    d = {"subreddit": submission["subreddit"], "text": submission["selftext"], "length": len(doc)}
                    l.append(d)
        for comment in comments_data["data"]:
            if "body" in comment.keys():
                doc = nlp(comment["body"])
                if len(doc) >= 100:
                    num_posts += 1
                    num_comments += 1
                    lengths.append(len(doc))
                    d = {"subreddit": comment["subreddit"], "text": comment["body"], "length": len(doc)}
                    l.append(d)
        posts[author] = l

    with open("./logs/nonpsychotic_post_scraper_log.txt", "w") as l:
        l.write("Number of total posts: " + str(num_posts) + "\n")
        l.write("Number of comments: " + str(num_comments) + "\n")
        l.write("Number of submissions: " + str(num_submissions) + "\n")
        l.write("Mean length of posts: " + str(sum(lengths) / len(lengths)) + "\n")
        l.write("Standard deviation of post lengths: " + str(statistics.stdev(lengths)) + "\n")

    with open("./data/raw/nonpsychotic_posts.pickle", "wb") as p:
        pickle.dump(posts, p)