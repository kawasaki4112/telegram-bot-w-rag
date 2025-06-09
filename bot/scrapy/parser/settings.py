BOT_NAME = 'parser'
SPIDER_MODULES = ['bot.scrapy.parser.spiders']
NEWSPIDER_MODULE = 'bot.scrapy.parser.spiders'
ROBOTSTXT_OBEY = True
ITEM_PIPELINES = {'bot.scrapy.parser.pipelines.EmbeddingPipeline': 300}