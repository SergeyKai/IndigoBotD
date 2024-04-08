import logging
from datetime import timedelta, datetime

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util
from telebot import TeleBot

from bot.models import SessionRecord

logger = logging.getLogger(__name__)


def notify_task():
    """
    Задача для отправки оповещений пользователям записанным на занятие
    :return: None
    """
    current_datetime = timezone.now()
    session_records = SessionRecord.objects.filter(
        Q(session__date__gt=current_datetime.date()) |
        Q(session__date=current_datetime.date(), session__time__gte=current_datetime.time()),
        notified=False
    )
    bot = TeleBot(settings.TOKEN_BOT)
    print(session_records)

    for session_record in session_records:

        session_datetime = timezone.make_aware(
            datetime.combine(session_record.session.date, session_record.session.time))

        time_difference = session_datetime - current_datetime

        if time_difference <= timedelta(hours=1):
            user = session_record.user
            session = session_record.session
            message = (f'Занятие: {session.title}\n'
                       f'Направление: {session.direction.title}\n'
                       f'Специалист: {session.specialist.first_name} {session.specialist.last_name}\n'
                       f'Дата: {session.date} Время: {session.time}')

            bot.send_message(user.tg_id, str(message))
    print('=' * 30)
    print('=' * 30)


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)

        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            notify_task,
            trigger=CronTrigger(minute="*/5"),  # Каждые 5 минут
            id="notify_task",  # `id` идетификатор задачи. Для каждой задачи должен быть уникален
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'another_job'.")

        try:
            logger.info("Starting scheduler...")
            if not scheduler.running:
                scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
