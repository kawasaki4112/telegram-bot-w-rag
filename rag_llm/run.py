from llama_cpp import Llama

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sentence_transformers import SentenceTransformer

model_path = "models/model-Q2_K.gguf"
llm = Llama(model_path=model_path, n_gpu_layers=40, n_ctx=512, n_batch=512)
emb_model = SentenceTransformer('all-MiniLM-L6-v2')

DATABASE_URL = "sqlite:///embeddings.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Embedding(Base):
    __tablename__ = 'embeddings'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    data = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def find_rel_d(query, top_k=3):
    query_embedding = emb_model.encode(query).reshape(1, -1)
    embeddings = session.query(Embedding).all()
    print(f"\n\n{query_embedding}\n\n")
    
    if not embeddings:
        return []

    document_embeddings = []
    documents = []

    for emb in embeddings:
        document_embeddings.append(emb.embedding)
        documents.append({'url': emb.url, 'data': emb.data})

    document_embeddings = np.array(document_embeddings)
    similarities = cosine_similarity(query_embedding, document_embeddings).flatten()
    sorted_indices = np.argsort(similarities)[::-1]

    return [
        {'url': documents[idx]['url'], 'data': documents[idx]['data'], 'similar': similarities[idx]}
        for idx in sorted_indices[:top_k]
    ]

def main():
    question = "сколько программ магистратуры"
    rel = find_rel_d(question)

    context_str = "\n".join(f"{doc['url']}: {doc['data']}" for doc in rel)
    rules = (
        "1. Отвечать только на тему СВФУ (Северо-Восточный федеральный университет). "
        "2. Отвечать официальным тоном."
    )

    prompt = f"""Правила: {rules}
    Контекст: {context_str}
    Пользователь: {question}
    Оператор:"""

    response = llm(
        prompt=prompt,
        max_tokens=512,
        temperature=0.7,
        top_p=0.9,
        repeat_penalty=1.1,
        presence_penalty=0.5
    )

    print(prompt)
    print(response["choices"][0]["text"].strip())

if __name__ == "__main__":
    main()