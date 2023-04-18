from django.http import HttpResponse
import json
from django.shortcuts import render
from django.core.cache.backends.locmem import _caches as cache
from django.http import JsonResponse

from appchat.models import Rooms, UserProfile, Message
from .serializers import RoomSerializer, UserProfileSerializer, MessageSerializer, UserSerializer
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView

from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, UserForm, ProfileForm


def rooms_reader():
    rooms = []
    for key in cache['us']:
        rooms.append(key)
    return rooms


def index(request):
    rooms = rooms_reader()
    return render(request, "appchat/index.html", context={'rooms': rooms})


def login_user(request):
    return render(request, 'registration/login.html')


def room(request, room_name):
    room_name = room_name.replace(' ', '_')
    return render(request, "appchat/chatbox.html", context={"room_name": room_name})


def rooms_return(request):
    rooms = rooms_reader()
    jsn = json.dumps(rooms)
    return HttpResponse(jsn)


def api_users(request):
    if request.method == 'GET':
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)


class ApiUsers(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ApiRooms(ModelViewSet):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer


class ApiMessage(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ApiUser(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login')


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserForm(instance=request.user, data=request.POST)
        profile_form = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'registration/profile.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'user': request.user})
