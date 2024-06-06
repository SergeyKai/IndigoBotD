from aiogram import Router
from aiogram.dispatcher.event.handler import HandlerObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.models import User
from bot.states import SignUpStatesGroup
from bot.utils.validators import validate_phone_number, normalize_phone_number

router = Router()


async def start_registration(income_data: CallbackQuery | Message,
                             state: FSMContext,
                             handled_obj: HandlerObject | None = None):
    if isinstance(income_data, CallbackQuery):
        await income_data.message.answer('Введите ваше имя')
    elif isinstance(income_data, Message):
        await income_data.answer('Здравствуйте, как к вам обращаться')

    if handled_obj:
        await state.update_data(handled_obj=handled_obj, handled_date=income_data)
    await state.set_state(SignUpStatesGroup.GET_NAME)


@router.message(SignUpStatesGroup.GET_NAME)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Введите номер телефона 📱')
    await state.set_state(SignUpStatesGroup.GET_PHONE_NUMBER)


@router.message(SignUpStatesGroup.GET_PHONE_NUMBER)
async def get_phone_number(message: Message, state: FSMContext):
    phone_number = message.text
    if validate_phone_number(phone_number):
        await User.create_async(
            name=(await state.get_data())['name'],
            tg_id=message.from_user.id,
            phone_number=normalize_phone_number(phone_number)
        )
        await message.answer('Вы успешно зарегистрированы')

        state_data = await state.get_data()
        handled_date = state_data.get('handled_date')
        handled_obj = state_data.get('handled_obj')
        await state.clear()
        if handled_obj:
            await handled_obj(handled_date, state)
    else:
        await message.answer('Не верный формат номера ☹')
        await message.answer('Попробуйте снова! \n'
                             'Пример формата: +7 999 999 99 99')
