from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe


class Rooms(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name='Комнаты')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class UserProfile(models.Model):
    rooms = models.OneToOneField(Rooms, on_delete=models.SET_NULL, null=True, verbose_name='Комната')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name='Профиль',
                                null=True)
    about = models.CharField(max_length=128, null=True, blank=True, default='', verbose_name='О себе')
    avatar = models.ImageField(max_length=None, upload_to='avatars', default='avatars/default.jpg', null=True,
                               blank=True, verbose_name='Аватар')
    online = models.BooleanField(default=False, verbose_name='Активен')

    def __str__(self):
        if self.about:
            says = self.about[:20]
        else:
            says = 'пока ничего не сказал'
        return f'{self.user} о себе {says}'

    def get_avatar(self):
        if not self.avatar:
            return 'avatars/default.jpg'
        return self.avatar.url

    def avatar_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % self.get_avatar())

    avatar_tag.short_description = 'Аватар'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    rooms = models.ForeignKey(Rooms, on_delete=models.CASCADE, verbose_name='Комнаты')
    text = models.CharField(max_length=255, verbose_name='Текст')

    def __str__(self):
        return f"{self.author}"

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
