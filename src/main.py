from google_play_scraper import app, reviews, Sort
import matplotlib.pyplot as plt
from collections import Counter

def safe(value):
     return value if value is not None else "N/A"

if __name__ == "__main__":
    app_id = "gov.mcmc.nexus"

    result = app(app_id)
    print("App:", result["title"])
    print("Downloads:", result["installs"])
    print("Rating Count:", safe(result["ratings"]))
    print("Score:", safe(result["score"]))
    print("Reviews:", safe(result["reviews"]))
    print("Released:", result["released"])

    print(result.get("histogram"))

    review_result, _ = reviews(
        app_id,
        lang="en",
        country="my",
        sort=Sort.NEWEST,
        count=1000
    )

    ratings = [r["score"] for r in review_result]

    rating_counts = Counter(ratings)

    # Ensure all ratings exist (1–5)
    stars = [1, 2, 3, 4, 5]
    values = [rating_counts.get(star, 0) for star in stars]

    for r in review_result:
        print("\nUser:", r["userName"])
        print("Rating:", r["score"])
        print("Date:", r["at"])
        print("Comment:", r["content"])

    plt.bar(stars, values)
    plt.title("User Rating Distribution")
    plt.xlabel("Stars")
    plt.ylabel("Number of Reviews")
    plt.xticks(stars)
    plt.show()