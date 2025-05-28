import os
import json
import numpy as np
from llama_cpp import Llama
from sklearn.metrics.pairwise import cosine_similarity

from ..database.requests import embedding_crud
from ..database.models import Embedding

MODEL_PATH = os.getenv('LLM_PATH', 'bot/llm/models/model-q4_K.gguf')
llm = Llama(model_path=MODEL_PATH, embedding=True, n_gpu_layers=40, n_ctx=512)

async def create_embeddings(file_path: str = 'bot/scrapy/parsed_data/output.json') -> None:
    """
    Загружает JSON-файл и создает эмбеддинги для новых записей.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            url = item['url']
            text = item['data']

            existing_record = await embedding_crud.get(url=url)
            if existing_record:
                continue

            embedding_response = llm.create_embedding(text)
            embedding_vector = embedding_response["embedding"][0]

            await embedding_crud.create(
                url=url,
                text=text,
                embedding=embedding_vector
            )

    except Exception as e:
        print(f"Ошибка при сохранении эмбеддингов: {e}")

async def search_relevant_data(query: str) -> list[dict]:
    """
    Ищет релевантные данные по запросу.
    """
    embedding = llm.create_embedding(query)
    if isinstance(embedding, dict) and "data" in embedding:
        query_embedding = embedding["data"][0]
    else:
        raise ValueError("Неверный формат эмбеддинга")

    embeddings = await embedding_crud.get_list()

    similarities = [
        {
            "url": emb.url,
            "data": emb.text,
            "similarity": cosine_similarity([query_embedding], [emb.embedding])[0][0]
        }
        for emb in embeddings
    ]

    sorted_results = sorted(similarities, key=lambda x: x["similarity"], reverse=True)
    return sorted_results

async def query_llm(question: str) -> str:
    relevant_docs = await search_relevant_data(question)

    context_str = "\n".join(f"{doc['url']}: {doc['data']}" for doc in relevant_docs[:5])  # топ-5
    rules = (
        "1. Отвечать только на тему СВФУ (Северо-Восточный федеральный университет). "
        "2. Отвечать официальным тоном."
    )

    prompt = f"""Правила: {rules}
Контекст: {context_str}
Пользователь: {question}
Оператор:"""

    response = await llm.async_call(
        prompt=prompt,
        max_tokens=512,
        temperature=0.7,
        top_p=0.9,
        repeat_penalty=1.1,
        presence_penalty=0.5
    )
    return response['choices'][0]['text']
