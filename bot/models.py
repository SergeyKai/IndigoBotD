from django.conf import settings
from django.db import models
from asgiref.sync import sync_to_async
import asyncio

from django.db.models import Q
from django.utils import timezone


class AsyncMixin:
    """
    Миксин для асинхронного запроса в БД на создание записи
    """

    @classmethod
    async def create_async(cls, **kwargs):
        obj = cls(**kwargs)
        await asyncio.to_thread(obj.save)
        return obj


class AsyncManager(models.Manager):
    """
    Менеджер асинхронных запросов в БД
    """

    async def all_async(self):
        queryset = self.all()
        return await sync_to_async(list)(queryset)

    async def filter_async(self, *args, **kwargs):
        queryset = self.filter(*args, **kwargs)
        return await sync_to_async(list)(queryset)

    async def filter_with_ordering_async(self, order_fields, *args, **kwargs):
        queryset = self.order_by(*order_fields).filter(*args, **kwargs)
        queryset_list = await sync_to_async(list)(queryset)
        return queryset_list


class Direction(models.Model):
    """
    Модель направлений
    """
    title = models.CharField(max_length=300, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    objects = AsyncManager()

    class Meta:
        verbose_name = 'Направление'
        verbose_name_plural = 'Направления'

    def __str__(self):
        return f"id: {self.pk} title: {self.title}"


class User(AsyncMixin, models.Model):
    """
    Модель клиентов
    """
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True)

    tg_id = models.BigIntegerField()

    objects = AsyncManager()

    def __str__(self):
        return f"id: {self.pk} phone number: {self.phone_number}"


class Specialization(models.Model):
    """
    Модель специализаций
    """
    name = models.CharField(max_length=300, verbose_name='Название')

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def __str__(self):
        return f"id: {self.pk} name: {self.name}"


class Specialist(models.Model):
    """
    Модель специалистов
    """
    first_name = models.CharField(max_length=300, verbose_name='Имя')
    last_name = models.CharField(max_length=300, verbose_name='Фамилия')

    link_on_site = models.URLField(verbose_name='Ссылка на сайте')

    specialization = models.ForeignKey(
        Specialization,
        related_name="specialists",
        on_delete=models.CASCADE,
        verbose_name='Специализация'
    )

    photo = models.ImageField(
        upload_to='specialists',
        default='specialists/specialist_default.png',
        verbose_name='Фото'
    )

    objects = AsyncManager()

    class Meta:
        verbose_name = 'Специалист'
        verbose_name_plural = 'Специалисты'

    def __str__(self):
        return f"id: {self.pk} first_name: {self.first_name} last_name: {self.last_name}"

    def get_full_path_photo(self):
        return f'{settings.MEDIA_ROOT}\\{self.photo}'

    @sync_to_async
    def get_specialization(self):
        return self.specialization

    async def get_info(self):
        await self.get_specialization()
        return (f'{self.first_name} {self.last_name}\n'
                f'Специализация: {self.specialization.name}')


class SessionAsyncManager(AsyncManager):
    """
    Менеджер асинхронных запросов в БД для модели Session
    """

    async def get_current_sessions(self, *args, **kwargs):
        current_datetime = timezone.now()
        queryset = self.order_by('date', 'time').filter(
            Q(date__gt=current_datetime.date()) |
            Q(date=current_datetime.date(), time__gte=current_datetime.time())
        )[:5]
        queryset_list = await sync_to_async(list)(queryset)
        return queryset_list


class Session(AsyncMixin, models.Model):
    """
    Модель занятий
    """
    title = models.CharField(max_length=300, verbose_name='Заголовок', null=True, blank=True, )
    direction = models.ForeignKey(
        Direction,
        related_name="sessions",
        on_delete=models.CASCADE,
        verbose_name='Направление',
    )
    date = models.DateField(null=True, verbose_name='Дата', )
    time = models.TimeField(null=True, verbose_name='Время', )

    specialist = models.ForeignKey(
        Specialist,
        related_name="sessions",
        on_delete=models.CASCADE,
        verbose_name='Специалист',
        null=True,
        blank=True,
    )

    objects = SessionAsyncManager()

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        ordering = ['-date', '-time']

    def __str__(self):
        return f"id: {self.pk} title: {self.title}"

    @sync_to_async
    def get_specialist(self):
        return self.specialist

    @sync_to_async
    def get_direction(self):
        return self.direction

    async def message_text(self):
        await self.get_direction()
        await self.get_specialist()

        _specialist = f'Специалист: {self.specialist.first_name} {self.specialist.last_name}\n'

        text = (f'Занятие: {self.title}\n'
                f'Направление: {self.direction.title}\n'
                f'{_specialist if _specialist is not None else ""}'
                f'Дата: {self.date} Время: {self.time}')
        return text


class SessionRecordAsyncManager(AsyncManager):
    """
    Менеджер асинхронных запросов в БД для модели Session
    """

    async def get_with_select_related(self, pk):
        queryset = self.select_related('user', 'session').get(pk=pk)
        queryset_list = await sync_to_async(list)(queryset)
        return queryset_list


class SessionRecord(AsyncMixin, models.Model):
    """
    Модель записей на занятия
    """
    user = models.ForeignKey(
        User,
        related_name="session_records",
        on_delete=models.CASCADE,
        verbose_name='Клиент',
    )
    session = models.ForeignKey(
        Session,
        related_name="session_records",
        on_delete=models.CASCADE,
        verbose_name='Занятие',
    )

    objects = SessionRecordAsyncManager()

    notified = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Запись на занятие'
        verbose_name_plural = 'Записи на занятия'

    def __str__(self):
        return f"id: {self.pk} user: {self.user_id} session: {self.session_id}"

    @sync_to_async
    def get_related(self):
        session = self.session
        user = self.user
        return session, user


class Location(models.Model):
    """
    Модель локаций
    """
    title = models.CharField(max_length=300, verbose_name='Название')
    address = models.CharField(max_length=500, verbose_name='Адрес')
    on_map_link = models.TextField(verbose_name='Ссылка на карту')
    on_site_link = models.TextField(verbose_name='Ссылка на сайт')

    objects = AsyncManager()

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return f"id: {self.pk} title: {self.title}"

    def get_info(self):
        return (f'{self.title}\n'
                f'{self.address}')


class Contacts(models.Model):
    """
    Модель контактов (для корректной работы в БД должна быть хотя бы 1 запись!)
    """
    phone_number = models.CharField(max_length=30, verbose_name='Номер телефона')
    email = models.EmailField(max_length=200, verbose_name='Адрес электронной почты')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f"id: {self.pk} phone_number: {self.phone_number} email: {self.email}"
