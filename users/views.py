from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages


# Create your views here.
def index(request):
    path = request.get_full_path()
    user = request.user
    is_authenticated = user.is_authenticated
    context = {"path": request.get_full_path(), "user": user, "is_authenticated": is_authenticated}
    if not is_authenticated:
        response = render(request, "users/index.html", context)
    else:
        response = HttpResponseRedirect(reverse("user_page"))
    return response


def user_page(request):
    path = request.get_full_path()
    user = request.user
    is_authenticated = user.is_authenticated
    context = {"path": request.get_full_path(), "user": user, "is_authenticated": is_authenticated, "friends": []}
    if not is_authenticated:
        response = render(request, "users/index.html", context)
    else:
        context['friends'] = user.friends.all()
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


def profile(request):
    path = request.get_full_path()
    html = f'<html lang="en"><body>Profile view triggered. The path {path} was'
    html += "requested.</body></html>"
    return HttpResponse(html)

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
    response = HttpResponseRedirect(reverse("index"))
    return response

def add_friend(request):
    user = request.user
    search_method = request.POST["search_method"]
    search_term = request.POST.get(search_method,None)
    if not search_term:
        msg = "You must provide a handle or email."
        messages.add_message(request, messages.ERROR, msg)
    else:
        friend, msg, msg_type = user.lookup_user(search_term, search_method)
        messages.add_message(request, msg_type, msg)
        if msg_type == messages.SUCCESS:
            user.add_friend(friend)
    response = HttpResponseRedirect(reverse("user_page"))
    return response
    """ add this stuff later 
    if request.method != "POST":
        msg = "Invalid request method."
        messages.add_message(request, messages.INFO, msg)
    elif not user.is_authenticated:
        msg = "You must be logged in to add a friend."
        messages.add_message(request, messages.INFO, msg)
    """