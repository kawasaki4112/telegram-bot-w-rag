import asyncio, logging, os, sys, colorama
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher


from bot.data.config import BOT_SCHEDULER
from bot.routers import register_all_routers
from bot.database.models import async_main as db_async_main
from bot.database.requests import get_admins
from bot.utils.misc.bot_commands import set_commands
from bot.middlewares import register_all_middlwares
from bot.utils.misc.bot_commands import set_commands
from bot.utils.misc.bot_logging import bot_logger

#from rag_llm.run import

# async def scheduler_start(bot: Bot):
#     BOT_SCHEDULER.add_job(func,trigger="cron", day=1)

async def main() -> None:
    # BOT_SCHEDULER.start()
    await db_async_main()
    load_dotenv()
    dp = Dispatcher()
    bot = Bot(token=os.getenv('TOKEN'))
    
    register_all_middlwares(dp)
    register_all_routers(dp)
    
    await set_commands(bot)
    
    bot_logger.warning("BOT WAS STARTED")
    print(colorama.Fore.LIGHTYELLOW_EX + f"~~~~~ Bot was started - @{(await bot.get_me()).username} ~~~~~")
    print(colorama.Fore.LIGHTBLUE_EX + "~~~~~ TG developer - @arsan_duolaj ~~~~~")
    print(colorama.Fore.RESET)
    if len(await get_admins()) == 0:
        print(colorama.Fore.LIGHTGREEN_EX + '***** ENTER ADMIN IN DB *****')
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        logging.basicConfig(level=logging.INFO)
    except(KeyboardInterrupt, SystemExit):
        bot_logger.warning("Bot was stopped")
    finally:
        if sys.platform.lower().startswith("win"):
            os.system("cls")
        else:
            os.system("clear")
    