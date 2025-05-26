from rag_llm.llm import llm
from rag_llm.embedding import find_rel_d

async def request(question: str) -> str:
    rel = await find_rel_d(question)

    context_str = "\n".join(f"{doc['url']}: {doc['data']}" for doc in rel)
    rules = (
        "1. Отвечать только на тему СВФУ (Северо-Восточный федеральный университет). "
        "2. Отвечать официальным тоном."
    )

    prompt = f"""Правила: {rules}
                 Контекст: {context_str}
                 Пользователь: {question}
                 Оператор:"""
    
    response = await llm(
        prompt=prompt,
        max_tokens=512,
        temperature=0.7,
        top_p=0.9,
        repeat_penalty=1.1,
        presence_penalty=0.5
    )
    return response["choices"][0]["text"].strip()
