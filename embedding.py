import json
import logging
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, Column, Integer, String, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)

# Инициализация модели
emb_model = SentenceTransformer('all-MiniLM-L6-v2')

# Настройка базы данных
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

def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_and_save_embeddings(data):
    session = Session()
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
