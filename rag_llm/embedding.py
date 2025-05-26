import json
import logging
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)

# Инициализация модели
emb_model = SentenceTransformer('all-MiniLM-L6-v2')


def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_and_save_embeddings(data):
    try:
        for item in data:
            url = item['url']
            text = item['data']

            existing_record = session.query(Embedding).filter_by(url=url).first()
            if existing_record:
                logging.info(f"{url} - уже был")
                continue

            embedding = emb_model.encode(text).tolist()

            new_embedding = Embedding(url=url, data=text, embedding=embedding)
            session.add(new_embedding)

        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Ошибка при сохранении эмбеддингов: {e}")
    finally:
        session.close()

def main():
    data = load_data_from_json('output.json')
    create_and_save_embeddings(data)

if __name__ == "__main__":
    main()
