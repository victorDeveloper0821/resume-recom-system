from pymongo import MongoClient

mongo_client = None
mongo_db = None
resumes_collection = None


def init_extensions(app):
    global mongo_client, mongo_db, resumes_collection
    try:
        mongo_uri = app.config.get("MONGO_URI")
        mongo_db_name = app.config.get("MONGO_DB_NAME")

        mongo_client = MongoClient(mongo_uri)
        mongo_db = mongo_client[mongo_db_name]
        resumes_collection = mongo_db["resumes"]

        print(f"[MongoDB] Connected to {mongo_db_name} at {mongo_uri}")

    except Exception as e:
        print(f"[MongoDB Error] Could not connect: {e}")
        raise

# 供其他模組使用的 getter（推薦做法）
def get_resume_collection():
    if resumes_collection is None:
        raise RuntimeError("MongoDB not initialized. Call init_extensions() first.")
    return resumes_collection