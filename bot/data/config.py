from apscheduler.schedulers.asyncio import AsyncIOScheduler

BOT_TIMEZONE = "Asia/Yakutsk"
BOT_SCHEDULER = AsyncIOScheduler(timezone=BOT_TIMEZONE)  
DB_PATH = "bot/data/db.sqlite3"