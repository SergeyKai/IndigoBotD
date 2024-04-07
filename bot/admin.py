from django.contrib import admin

from . import models


@admin.register(models.Direction)
class DirectionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    pass


@admin.register(models.SessionRecord)
class SessionRecordAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    pass


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Contacts)
class ContactsAdmin(admin.ModelAdmin):
    pass
