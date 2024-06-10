from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message()
async def non_existent_commands_handler(message: Message):
    """ обработчик несуществующих команд """
    if message.text != '/start':
        await message.answer('Я вас не понимаю ☹')
