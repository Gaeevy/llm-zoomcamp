from dotenv import load_dotenv

load_dotenv()

import logging
from common import setup_logging
from elastic_search import search_knn
from llm import llm

setup_logging()

logger = logging.getLogger(__name__)


def rag(user_question: str) -> str:
    results = search_knn(user_question)
    llm_response = llm(user_question, [result["_source"] for result in results])
    return llm_response


if __name__ == '__main__':
    user_question = "Win or mac?"
    response = rag(user_question)
    print(f"User question: {user_question} \n RAG response: {response}")




