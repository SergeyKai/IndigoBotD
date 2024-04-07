from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..filters import IsRegistered
from ..models import Session, User, SessionRecord

from .. import keyboards as kb
from ..models import Direction
from ..states import SignUpStatesGroup

router = Router()


@router.message(F.text == kb.MainKeyboardBtnTexts.DIRECTIONS)
@router.message(Command('directions'))
async def directions(message: Message):
    """
    обработчик команды directions
    выводит список направлений
    """
    await message.answer('Наши направления', reply_markup=await kb.directions())


@router.callback_query(F.data.startswith('direction__'))
async def direction_info(callback: CallbackQuery, state: FSMContext):
    """
    обработчик колбека direction__
    выводит информацию по выбронному направлению
    """
    direction_id = int(callback.data.split('__')[-1])
    direction = await Direction.objects.aget(pk=direction_id)
    await callback.message.answer(direction.description, reply_markup=await kb.sign_up_keyboard(direction_id))
    await callback.answer(direction.title)


@router.callback_query(F.data.startswith('sign_up_direction__'), IsRegistered())
async def sig_up_direction(callback: CallbackQuery, state: FSMContext):
    """
    обработчик колбека sign_up_direction__
    запускает процесс запси пользователя на занятие
    """
    direction_id = int(callback.data.split('__')[-1])

    sessions = await Session.objects.get_current_sessions('date', direction=direction_id)

    await callback.message.answer('Выберите удобную для вас дату и время ☺', reply_markup=kb.cancel_keyboard)

    for session in sessions:
        await callback.message.answer(
            text=await session.message_text(),
            reply_markup=await kb.sign_up_keyboard(session.pk, 'sign_up_session__')
        )
    await state.set_state(SignUpStatesGroup.SELECT_SESSION)
    await callback.answer('Занятия')


@router.callback_query(F.data.startswith('sign_up_session__'), SignUpStatesGroup.SELECT_SESSION)
async def sig_up_direction(callback: CallbackQuery, state: FSMContext):
    """
    обработчик колбека sign_up_session__
    создание объекта записи на занятие
    """
    session_id = int(callback.data.split('__')[-1])
    user = await User.objects.aget(tg_id=callback.from_user.id)
    session = await Session.objects.aget(pk=session_id)
    await SessionRecord.create_async(
        user=user,
        session=session,
    )
    await callback.message.answer(
        f'Вы успешно записаны на занятие:\n{await session.message_text()}',
        reply_markup=kb.main_keyboard
    )
    await state.clear()


@router.message(F.text == kb.MainKeyboardBtnTexts.SIGN_UP, IsRegistered())
async def sig_up_direction(message: Message, state: FSMContext):
    """
    обработчик нажатия на кнопку записи
    запускает процесс запси пользователя на занятие
    """
    await message.answer('Выберите направление', reply_markup=await kb.directions('sign_up_direction__'))
