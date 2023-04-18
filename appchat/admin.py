from django.contrib import admin

from .models import Rooms, Message, UserProfile


@admin.register(Rooms)
class RoomsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_filter = ('id', 'name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'rooms', 'text')
    list_display_links = ('id', 'author', 'rooms', 'text')
    list_filter = ('id', 'author')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'rooms', 'user', 'about', 'avatar_tag', 'online',)
    list_display_links = ('id', 'user', 'rooms',)
    list_filter = ('id', 'user')
