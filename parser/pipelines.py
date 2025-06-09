from bot.database.requests import embedding_crud
from bot.llm.llm import create_embedding

class EmbeddingPipeline:
    async def process_item(self, item, spider):
        text = item['text']
        embedding = await create_embedding(text)
        await embedding_crud.create(
                url=item['url'],
                text=text,
                embedding=embedding,
            )
        return item