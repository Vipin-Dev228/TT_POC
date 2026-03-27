from pymongo import MongoClient

# Replace with your MongoDB connection string
MONGO_URI = "mongodb://dbadminroot:KK77UUhYT&hw@stagingdb.talenttrail.ai:27017/talent-trail-dev?authSource=admin"


def fetch_candidates(
    bucket: str = "Software Development", job_title: str = "Software Engineer"
):
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)

        # Select database
        db = client["talent-trail-dev"]

        # Select collection
        collection = db["candidates"]

        # Fetch top 100 records
        # (by default order = insertion order unless sorted)
        records = collection.find(
            {"category": bucket, "currentJobTitle": job_title}
        ).limit(100)

        # Convert cursor to list
        result = list(records)
        print(f"Total records found: {len(result)}")

        return result

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    fetch_candidates()
