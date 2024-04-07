import asyncio
from django.core.management.base import BaseCommand

from bot.main_bot import main


class Command(BaseCommand):
    help = "Run bot"

    def handle(self, *args, **options):
        asyncio.run(main())
