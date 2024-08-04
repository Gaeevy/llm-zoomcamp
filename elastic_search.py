from elasticsearch import Elasticsearch
from embeddings import encode, vector_size
from common import load_docs_with_ids
import logging

logger = logging.getLogger(__name__)

INDEX_NAME = "course-qa"
_es_client = Elasticsearch("http://localhost:9200")


def init_search_index(index_name: str, index_settings: dict):
    logger.info(f"Initializing search index {index_name}...")
    _es_client.indices.delete(index=index_name, ignore_unavailable=True)
    _es_client.indices.create(index=index_name, body=index_settings)


def index_documents(documents: list[dict], index_name: str):
    from tqdm import tqdm

    logger.info(f"Indexing {len(documents)} documents...")
    for doc in tqdm(documents):
        try:
            _es_client.index(index=index_name, document=doc)
        except Exception as e:
            print(e)


def form_knn_query(user_question_vector, field="qa_vector", k=5, num_candidates=10000):
    knn_query = {
        "field": field,
        "query_vector": user_question_vector,
        "k": k,
        "num_candidates": num_candidates,
    }
    return knn_query


def search_knn(user_question, index_name: str = INDEX_NAME, field="qa_vector", k=5, num_candidates=10000):
    logger.info(f"Searching for similar questions to: \"{user_question}\"")
    user_question_vector = encode(user_question)
    response = _es_client.search(
        index=index_name,
        knn=form_knn_query(user_question_vector, field, k, num_candidates),
        size=5,
        source=["question", "answer", "id"],
    )
    return response["hits"]["hits"]


def ingest_elastic_search_data():
    logger.info("Ingesting data into ElasticSearch...")
    from tqdm import tqdm

    documents = load_docs_with_ids()
    logger.info("Calculating embeddings for documents...")
    for doc in tqdm(documents):
        doc["answer"] = doc.pop("text")
        doc["qa_vector"] = encode(doc["question"] + " " + doc["answer"])

    logger.info("Initializing search index...")
    index_name = INDEX_NAME
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "answer": {"type": "text"},
                "section": {"type": "text"},
                "question": {"type": "text"},
                "course": {"type": "keyword"} ,
                "qa_vector": {"type": "dense_vector", "dims": vector_size, "index": True, "similarity": "cosine"},
            }
        }
    }
    init_search_index(index_name, index_settings)
    index_documents(documents, index_name)
    logger.info("Data ingestion complete.")