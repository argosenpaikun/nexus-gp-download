from google_play_scraper import app, reviews, Sort
from collections import Counter
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway
import os
import time

PUSHGATEWAY = os.getenv("PUSHGATEWAY", "pushgateway:9091")
JOB_NAME = "google_play_scrapper"

def safe(value):
     return value if value is not None else 0

def collect_metrics():
        app_id = "gov.mcmc.nexus"

        result = app(app_id)

        review_result, _ = reviews(
             app_id,
             lang="en",
             country="my",
             sort=Sort.NEWEST,
             count=1000
        )

        ratings = [r["score"] for r in review_result]
        rating_counts = Counter(ratings)

        registry = CollectorRegistry()

        # App-level metrics
        download = Gauge("app_downloads", "Total Installs", registry=registry)
        rating_count = Gauge("app_rating_count", "Total Rating Count", registry=registry)
        score = Gauge("app_score", "Average Score", registry=registry)
        review_count = Gauge("app_reviews", "Total Reviews", registry=registry)

        # Rating distribution metrics
        rating_gauge = Gauge(
             "app_rating_distribution",
             "Distribution of Ratings",
             ["stars"],
             registry=registry
        )

        for star in [1, 2, 3, 4, 5]:
            rating_gauge.labels(stars=str(star)).set(rating_count.get(star, 0))

        # Push to Pushgateway
        push_to_gateway(PUSHGATEWAY, job=JOB_NAME, registry=registry)

if __name__ == "__main__":
      while True:
            try:
                  collect_metrics()
                  print("Metrics pushed successfully")
            except Exception as e:
                  print("Error: ", e)

            time.sleep(300) # run every 5 minutes