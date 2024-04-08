from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from .. import keyboards as kb
from ..models import Specialist, Location, Contacts

router = Router()


@router.message(CommandStart())
@router.message(F.text == kb.MainKeyboardBtnTexts.CANCEL)
@router.message(F.text == kb.MainKeyboardBtnTexts.MAIN_MENU)
async def start(message: Message, state: FSMContext):
    """ обработчик команды start
        запуск бота / приветственное сообщение
    """
    await state.clear()
    await message.answer('Привет!', reply_markup=kb.main_keyboard)


@router.message(F.text == kb.MainKeyboardBtnTexts.ABOUT)
async def about(message: Message):
    await message.answer('🙂', reply_markup=kb.about_keyboard)


@router.message(F.text == kb.MainKeyboardBtnTexts.OUR_SPECIALISTS)
async def our_specialists(message: Message):
    specialists = await Specialist.objects.all_async()
    for specialist in specialists:
        await message.answer_photo(
            photo=FSInputFile(specialist.get_full_path_photo()),
            caption=await specialist.get_info(),
            reply_markup=await kb.specialist_keyboard(specialist)
        )


@router.message(F.text == kb.MainKeyboardBtnTexts.OUR_LOCATIONS)
async def our_locations(message: Message):
    locations = await Location.objects.all_async()
    for location in locations:
        await message.answer(
            location.get_info(),
            reply_markup=await kb.location_keyboard(location)
        )


@router.message(F.text == kb.MainKeyboardBtnTexts.OUR_CONTACTS)
async def our_contacts(message: Message):
    contacts = await Contacts.objects.aget(pk=1)
    await message.answer(f'{contacts.phone_number}\n{contacts.email}')
