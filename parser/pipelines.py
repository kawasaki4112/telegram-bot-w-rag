from scrapy.exceptions import DropItem
from bot.database.requests import embedding_crud
from bot.llm.llm import create_embedding

class DuplicatesPipeline:
    async def process_item(self, item, spider):
        url = item['url']
        exists = await embedding_crud.get(url=url)
        if exists:
            spider.logger.info(f"URL {url} уже парсен — пропускаем")
            raise DropItem(f"Duplicate URL: {url}")
        return item

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