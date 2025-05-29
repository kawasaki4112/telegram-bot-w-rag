BOT_NAME = 'rag_crawler'

SPIDER_MODULES = ['rag_crawler.spiders']
NEWSPIDER_MODULE = 'rag_crawler.spiders'

# Директория для хранения состояния (dupefilter + очередь)
JOBDIR = 'crawls/rag_spider_job'  

# Оставляем только текст (минимум логов, чтобы не засорять)
LOG_LEVEL = 'INFO'
