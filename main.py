import requests
from openai import OpenAI
from dotenv import load_dotenv

import minsearch as ms

load_dotenv()


def prepare_docs() -> list[dict]:
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


def prepare_in_memory_index(documents: list[dict]) -> ms.Index:
    index = ms.Index(
        text_fields=["question", "text", "section"],
        keyword_fields=["course"]
    )
    index.fit(documents)
    return index


def search_by_query(query: str, index: ms.Index) -> list[dict]:
    boost = {'question': 3.0, 'section': 0.5}
    results = index.search(
        query=query,
        filter_dict={'course': 'data-engineering-zoomcamp'},
        boost_dict=boost,
        num_results=5
    )
    return results


def build_prompt(query: str, search_results: list[dict]) -> str:
    prompt_template = """
    You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
    Use only the facts from the CONTEXT when answering the QUESTION.

    QUESTION: {question}

    CONTEXT: 
    {context}
    """.strip()

    context = ""
    for doc in search_results:
        context += f"section: {doc['section']}\nquestion: {doc['question']}\nanswer: {doc['text']}\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(prompt: str, client: OpenAI) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def rag(query: str, client: OpenAI) -> str:
    index = prepare_in_memory_index(prepare_docs())
    search_results = search_by_query(query, index)
    prompt = build_prompt(query, search_results)
    answer = llm(prompt, client)
    return answer


def main():
    client = OpenAI()
    query = 'the course has already started, can I still enroll?'
    answer = rag(query, client)
    print(answer)


if __name__ == '__main__':
    main()


