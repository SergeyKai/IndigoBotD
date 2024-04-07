from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.handlers.user_handlers import start_registration
from bot.models import User


class IsRegistered(BaseFilter):

    async def __call__(self, income_data: CallbackQuery | Message, state: FSMContext, *args, **kwargs):
        try:
            user = await User.objects.aget(tg_id=income_data.from_user.id)
            return True
        except User.DoesNotExist:
            await start_registration(income_data, state, kwargs.get('handler').callback)
            return False
