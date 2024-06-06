from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message()
async def non_existent_commands_handler(message: Message):
    """ обработчик несуществующих команд """
    await message.answer('Я тебя не понимаю ☹')
