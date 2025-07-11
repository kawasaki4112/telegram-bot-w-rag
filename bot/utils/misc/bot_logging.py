import logging

import colorlog


PATH_LOGS = "logs.log"
bot_logger = logging

bot_logger.getLogger("aiosqlite").setLevel(logging.WARNING)

# Формат логгирования
log_formatter_file = bot_logger.Formatter("%(levelname)s | %(asctime)s | %(filename)s:%(lineno)d | %(message)s")
log_formatter_console = colorlog.ColoredFormatter(
    "%(purple)s%(levelname)s %(blue)s|%(purple)s %(asctime)s %(blue)s|%(purple)s %(filename)s:%(lineno)d %(blue)s|%(purple)s %(message)s%(red)s",
    datefmt="%d-%m-%Y %H:%M:%S",
)

# Логгирование в файл logs.log
file_handler = bot_logger.FileHandler(PATH_LOGS, "w", "utf-8")
file_handler.setFormatter(log_formatter_file)
file_handler.setLevel(bot_logger.INFO)

# Логгирование в консоль
console_handler = bot_logger.StreamHandler()
console_handler.setFormatter(log_formatter_console)
console_handler.setLevel(bot_logger.INFO)

# Подключение настроек логгирования
bot_logger.basicConfig(
    format="%(levelname)s | %(asctime)s | %(filename)s:%(lineno)d | %(message)s",
    handlers=[
        file_handler,
        console_handler
    ]
)
