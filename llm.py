from openai import OpenAI

_client = OpenAI()


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
        context += f"question: {doc['question']}\nanswer: {doc['answer']}\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt


def llm(user_question, context) -> str:
    prompt = build_prompt(user_question, context)
    response = _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
