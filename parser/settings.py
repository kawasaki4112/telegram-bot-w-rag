BOT_NAME = 'parser'
SPIDER_MODULES = ['parser.spiders']
NEWSPIDER_MODULE = 'parser.spiders'
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {
    'parser.pipelines.DuplicatesPipeline': 100,
    'parser.pipelines.EmbeddingPipeline': 300,
    }

DOWNLOADER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 100,
}
DELTAFETCH_ENABLED = True
DELTAFETCH_DIR = 'parser.deltafetch'