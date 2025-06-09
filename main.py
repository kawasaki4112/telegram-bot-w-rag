import asyncio, logging, os, sys, colorama
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'bot.scrapy.parser.settings')
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone
from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from bot.routers import register_all_routers
from bot.database.models import async_main
from bot.middlewares import register_all_middlwares
from bot.utils.misc.bot_logging import bot_logger
from bot.scrapy.parser.spiders.full_spider import FullSpider

async def run_parser():
    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(FullSpider)
        process.start()
    except Exception:
        print(colorama.Fore.LIGHTRED_EX + "~~~~~ Ошибка при выполнении парсинга ~~~~~")
        bot_logger.exception("Ошибка при выполнении парсинга")

def schedule_parser():
    scheduler = AsyncIOScheduler(timezone=timezone(os.getenv('TIMEZONE', 'Asia/Yakutsk')))
    scheduler.add_job(run_parser, 'cron', day_of_week='mon', hour=1, minute=0, second=0)
    scheduler.start()

async def main() -> None:
    try:        
        load_dotenv()
        await async_main()
        dp = Dispatcher()
        bot = Bot(token=os.getenv('TOKEN'))
        register_all_middlwares(dp)
        register_all_routers(dp)
        await run_parser()
        schedule_parser()
        
        bot_logger.warning("BOT WAS STARTED")
        print(colorama.Fore.LIGHTYELLOW_EX + f"~~~~~ Bot was started - @{(await bot.get_me()).username} ~~~~~")
        print(colorama.Fore.LIGHTBLUE_EX + "~~~~~ TG developer - @arsan_duolaj ~~~~~")
        print(colorama.Fore.RESET)
        await dp.start_polling(bot)
        
    except Exception:
        print(colorama.Fore.LIGHTRED_EX + "~~~~~ Bot was stopped due to an error ~~~~~")
        bot_logger.exception("Bot was stopped due to an error")
        

if __name__ == "__main__":
    try:
        asyncio.run(main())
        logging.basicConfig(level=logging.DEBUG)
    except(KeyboardInterrupt, SystemExit):
        bot_logger.warning("Bot was stopped")
    finally:
        if sys.platform.lower().startswith("win"):
            os.system("cls")
        else:
            os.system("clear")
