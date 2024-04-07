from django.conf import settings
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
import logging

from .commands import Commands
from .handlers.main_handlers import router as main_router
from .handlers.user_handlers import router as user_router
from .handlers.directions_handlers import router as directions_router


async def bot_start(bot: Bot) -> None:
    """ функция срабатывает при запуске бота """
    await Commands.set_commands(bot)


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.TOKEN_BOT, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.startup.register(bot_start)

    dp.include_routers(
        main_router,
        user_router,
        directions_router,
    )

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
