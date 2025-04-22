# search_resume.py
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from bson import ObjectId

mongo_client = MongoClient("mongodb+srv://austin:81WJm8UEJnKkN4jr@recommend.ssgbnnu.mongodb.net/?retryWrites=true&w=majority&appName=recommend")
db = mongo_client["resume_db"]
collection = db["resumes"]
model = SentenceTransformer('all-MiniLM-L6-v2')

def ensure_text_index():
    index_info = collection.index_information()
    if not any('text' in index.get('key', [])[0] for index in index_info.values()):
        collection.create_index([("Summary", "text")])

def semantic_search(query, top_n=20):
    query_vec = model.encode(query).tolist()
    return list(collection.aggregate([
        {
            "$vectorSearch": {
                "index": "default",
                "path": "embedded_vector",
                "queryVector": query_vec,
                "numCandidates": 2484,
                "limit": top_n
            }
        }
    ]))

def keyword_search(query, top_n=20):
    return list(collection.find(
        {"$text": {"$search": query}},
        {"score": {"$meta": "textScore"}, "Summary": 1}
    ).sort([("score", {"$meta": "textScore"})]).limit(top_n))

def reciprocal_rank_fusion(sem_results, kw_results, k=60):
    scores = {}
    for results in (sem_results, kw_results):
        for rank, doc in enumerate(results):
            doc_id = str(doc["_id"])
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
            doc["rrf_score"] = scores[doc_id]
    all_docs = {str(doc["_id"]): doc for doc in sem_results + kw_results}
    for doc_id in scores:
        all_docs[doc_id]["rrf_score"] = scores[doc_id]
    return sorted(all_docs.values(), key=lambda x: -x["rrf_score"])

def search_and_format(query):
    ensure_text_index()
    sem = semantic_search(query)
    kw = keyword_search(query)
    fused = reciprocal_rank_fusion(sem, kw)
    summary = "\n\n".join([
        f"ID: {str(doc['_id'])}\nSummary: {doc.get('Summary', '[No Summary]')}\nScore: {doc['rrf_score']:.4f}"
        for doc in fused[:5]
    ])
    return summary
