import os
import json
import asyncio
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

from ..database.requests import embedding_crud, request_crud
from ..database.models import Embedding
 
MODEL_PATH = os.getenv('LLM_PATH', 'bot/llm/models/model-q4_K.gguf')
llm = Llama(model_path=MODEL_PATH, n_gpu_layers=-1, n_ctx=12000, n_batch=2048)
embedder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


async def create_embedding(text: str) -> list[float]:
    emb = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: embedder.encode(text, show_progress_bar=False)
    )
    return emb.tolist()

async def search_relevant_data(query: str, top_k: int = 5) -> list[dict]:
 
    query_vec = embedder.encode(query, show_progress_bar=False)
    query_vec = np.array([query_vec]).astype('float32')
    faiss.normalize_L2(query_vec)
 
    embeddings = await embedding_crud.get_list()
    if not embeddings:
        return []
 
    vectors = np.array([emb.embedding for emb in embeddings]).astype('float32')
    faiss.normalize_L2(vectors)
 
    index = faiss.IndexFlatIP(vectors.shape[1])  
    index.add(vectors)
    distances, indices = index.search(query_vec, top_k)

    results = []
    for score, idx in zip(distances[0], indices[0]):
        emb = embeddings[idx]
        results.append({
            "url": emb.url,
            "data": emb.text,
            "similarity": float(score)
        })

    return results


async def query_llm(question: str, tg_id: int) -> str:
    tema = os.getenv('SITE_URL')
    relevant = await search_relevant_data(question)
    context_str = "\n".join(f"{d['url']}: {d['data']}" for d in relevant)
    rules = (
    "1. Отвечать только на тему "
    "2. Отвечать официальным тоном. "
    "3. Ничего не придумывать, если не знаешь ответа или если в контексте нет нужной информации! "
    "4. Если не знаешь ответа, то отвечать, что не знаешь."
    )

    prompt = (
        f"Правила: {rules}\n"
        f"Контекст:\n{context_str}\n"
        f"Пользователь: {question}\n"
        f"Оператор:"
    )
    print("\n",prompt,"\n")
    response = llm(
        prompt=prompt,
        max_tokens=2048,
        temperature=0.7,
        top_p=0.9,
        repeat_penalty=1.1,
        presence_penalty=0.5,
        stop = ["\n\n", "### Конец ответа"]
    )
    await request_crud.create(
        question=question,
        answer=response['choices'][0]['text'],
        user_tg_id=tg_id
    )
    return response['choices'][0]['text']
