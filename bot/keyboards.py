from dataclasses import dataclass

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .models import Direction


@dataclass
class MainKeyboardBtnTexts:
    DIRECTIONS: str = 'Направления 📃'
    ABOUT: str = 'О нас'
    SIGN_UP: str = 'Записаться 📝'
    SUPPORT: str = 'Поддержка ⚙'
    CANCEL: str = 'Отмена ❌'
    MAIN_MENU: str = '⬅'

    OUR_SPECIALISTS = 'Наши специалисты 🤵'
    OUR_LOCATIONS = 'Наши локации 🌏'
    OUR_CONTACTS = 'Наши контакты 📞'


main_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=MainKeyboardBtnTexts.DIRECTIONS), KeyboardButton(text=MainKeyboardBtnTexts.SIGN_UP)],
        [KeyboardButton(text=MainKeyboardBtnTexts.ABOUT)],
        [KeyboardButton(text=MainKeyboardBtnTexts.SUPPORT)],
    ]
)

cancel_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=MainKeyboardBtnTexts.CANCEL)],
    ]
)

about_keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text=MainKeyboardBtnTexts.OUR_SPECIALISTS)],
        [KeyboardButton(text=MainKeyboardBtnTexts.OUR_LOCATIONS)],
        [KeyboardButton(text=MainKeyboardBtnTexts.OUR_CONTACTS)],
        [KeyboardButton(text=MainKeyboardBtnTexts.MAIN_MENU)],
    ]
)


async def specialist_keyboard(obj):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text='Просмотреть на нашем сайте', url=obj.link_on_site))

    builder.adjust(1)

    return builder.as_markup()


async def location_keyboard(obj):
    builder = InlineKeyboardBuilder()

    builder.add(InlineKeyboardButton(text='Просмотреть на карте', url=obj.on_map_link))
    builder.add(InlineKeyboardButton(text='Просмотреть на нашем сайте', url=obj.on_site_link))

    builder.adjust(1)

    return builder.as_markup()


async def directions(callback_data_prefix: str = 'direction__') -> InlineKeyboardMarkup:
    """
    :param callback_data_prefix: приставка колбека
    :return: InlineKeyboardMarkup Клавиатрурклавиатуру направлений
    """
    direction_objects = await Direction.objects.all_async()
    builder = InlineKeyboardBuilder()

    for obj in direction_objects:
        builder.add(
            InlineKeyboardButton(text=obj.title, callback_data=f'{callback_data_prefix}__{obj.id}')
        )

    builder.adjust(1)

    return builder.as_markup()


async def sign_up_keyboard(pk: int, callback_data_prefix: str = 'sign_up_direction__') -> InlineKeyboardMarkup:
    """
    :param callback_data_prefix: приставка колбека
    :param pk: ID объекта модели
    :return: InlineKeyboardMarkup
    """
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(text=MainKeyboardBtnTexts.SIGN_UP, callback_data=f'{callback_data_prefix}__{pk}')

    )

    return builder.as_markup()
