from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.
def index(request):
    path = request.get_full_path()
    user = request.user
    is_authenticated = user.is_authenticated
    context = {"path": request.get_full_path(), "user": user, "is_authenticated": is_authenticated}
    response = render(request, "users/index.html", context)
    return response


def login(request):
    path = request.get_full_path()
    html = f'<html lang="en"><body>Login view triggered. The path {path} was requested.</body></html>'
    return HttpResponse(html)


def logout(request):
    path = request.get_full_path()
    html = f'<html lang="en"><body>Logout view triggered. The path {path} was requested.</body></html>'
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
