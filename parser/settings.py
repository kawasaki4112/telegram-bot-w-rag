BOT_NAME = 'parser'
SPIDER_MODULES = ['parser.spiders']
NEWSPIDER_MODULE = 'parser.spiders'
ROBOTSTXT_OBEY = False
ITEM_PIPELINES = {'parser.pipelines.EmbeddingPipeline': 300}