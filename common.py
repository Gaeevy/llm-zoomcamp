import json
import logging
import logging.config
import yaml


def setup_logging():
    with open("logging_config.yaml") as ymlfile:
        log_config = yaml.safe_load(ymlfile)
        # Set up the logger configuration
        logging.config.dictConfig(log_config)


def process_raw_docs() -> list[dict]:
    docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
    docs_response = requests.get(docs_url)
    documents_raw = docs_response.json()

    documents = []

    for course in documents_raw:
        course_name = course['course']

        for doc in course['documents']:
            doc['course'] = course_name
            documents.append(doc)

    return documents


def load_docs_with_ids() -> list[dict]:
    with open('data/documents-with-ids.json', 'r') as f:
        documents = json.load(f)
    return documents