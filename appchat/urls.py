from .views import ApiUsers, ApiRooms, ApiMessage, edit_user, SignUp, index, room, rooms_return, ApiUser, api_users, \
    login_user
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('rooms', ApiRooms)
router.register('profiles', ApiUsers)
router.register('message', ApiMessage)
router.register('user', ApiUser)


urlpatterns = [
    path('', index, name="index"),
    path('api/', include(router.urls)),
    path('roomsupdate/', rooms_return, name="rooms_return"),
    path('<str:room_name>/', room, name="room"),
    path('api_users/', api_users, name='api_users'),
    path('profile', edit_user, name='profile'),
    path('signup', SignUp.as_view(), name='signup'),
    path('login', login_user, name='login'),

]
