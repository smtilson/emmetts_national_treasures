from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from treasures.models import Treasure
from treasures.forms import TreasureCreationForm
from .serializers import CustomUserSerializer
from ..models import CustomUser, FriendshipRequest


# need to add things that check request.method and then redirect and what not.
# also flow control to check that users are valid or authenticated.


# Create your views here.
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


def index(request):
    user = request.user
    is_authenticated = user.is_authenticated
    context = {
        "path": request.get_full_path(),
        "user": user,
        "is_authenticated": is_authenticated,
    }
    if not is_authenticated:
        response = render(request, "users/index.html", context)
    else:
        response = HttpResponseRedirect(reverse("user_page"))
    return response


def user_page(request):
    user = request.user
    is_authenticated = user.is_authenticated
    id = getattr(user, "id", "no id found")
    treasure_form = TreasureCreationForm()
    context = {
        "path": request.get_full_path(),
        "user": user,
        "is_authenticated": is_authenticated,
        "friends": [],
        "id": id,
        "treasure_form": treasure_form,
        "treasure_list": list(Treasure.objects.filter(creator=user)),
    }
    if not is_authenticated:
        response = render(request, "users/index.html", context)
    else:
        context["friends"] = user.friends.all()
        response = render(request, "users/user_page.html", context)
    return response


def login(request):
    path = request.get_full_path()
    html = f'<html lang="en"><body>Login view triggered. The path {path} was requested.</body></html>'
    return HttpResponse(html)


def register(request):
    path = request.get_full_path()
    html = f'<html lang="en"><body>Register view triggered. The path {path} was requested.</body></html>'
    return HttpResponse(html)


# I think this will be handled on the front end by an axios patch request
def set_handle(request):
    user = request.user
    if not user.is_authenticated:
        msg = "You must be logged in to set your name."
        messages.add_message(request, messages.INFO, msg)
    elif request.method != "POST":
        msg = "Invalid request method."
        messages.add_message(request, messages.INFO, msg)
    else:
        user.handle = request.POST["handle"]
        user.save()
        msg = f"Handle set to {user.handle}."
        messages.add_message(request, messages.SUCCESS, msg)
    response = HttpResponseRedirect(reverse("user_page"))
    return response


def find_user(request):
    user = request.user
    search_method = request.POST["search_method"]
    search_term = request.POST.get(search_method, None)
    if not search_term:
        # this error should be better, maybe handled on the front end in terms of the response that is sent back
        raise ValueError("You must provide a handle or email.")
    return user.lookup_user(search_term, search_method)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_friend_request(request):
    # this is rudimentary and should be redone with friend requests or something like that.
    user = request.user
    friend, msg, msg_type = find_user(request)
    if msg_type == messages.SUCCESS:
        msg_type, msg = FriendshipRequest.create_request(user, friend)
    messages.add_message(request, msg_type, msg)
    response = HttpResponseRedirect(reverse("user_page"))
    return response
    """ add this stuff later 
    I believe this is now handled by the decorators above.
    if request.method != "POST":
        msg = "Invalid request method."
        messages.add_message(request, messages.INFO, msg)
    elif not user.is_authenticated:
        msg = "You must be logged in to add a friend."
        messages.add_message(request, messages.INFO, msg)
    """


def add_friend(request):
    return Response("<div>add_friend view triggered</div>")


def add_treasure(request):
    return Response("<div>add_treasure view triggered</div>")
