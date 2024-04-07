from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat


class Commands:
    """
    Основные команды бота
    """
    START_COMMAND = BotCommand(command='start', description='Запуск бота')
    HELP_COMMAND = BotCommand(command='help', description='Помощь')
    CANCEL_COMMAND = BotCommand(command='directions', description='Наши направления')

    @classmethod
    async def get_commands(cls):
        class_attributes = vars(cls)
        commands_list = [command for key, command in class_attributes.items() if
                         not key.startswith('_') and key.isupper()]
        return commands_list

    @classmethod
    async def set_commands(cls, bot: Bot):
        commands = await cls.get_commands()
        await bot.set_my_commands(commands, BotCommandScopeDefault())
