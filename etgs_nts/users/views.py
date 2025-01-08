from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    path = request.get_full_path()
    html = (
        f'<html lang="en"><body>Index view triggered. The path {path} was requested.</body></html>'
    )
    return HttpResponse(html)


def login(request):
    path = request.get_full_path()
    html = (
        f'<html lang="en"><body>Login view triggered. The path {path} was requested.</body></html>'
    )
    return HttpResponse(html)


def logout(request):
    path = request.get_full_path()
    html = (
        f'<html lang="en"><body>Logout view triggered. The path {path} was requested.</body></html>'
    )
    return HttpResponse(html)


def register(request):
    path = request.get_full_path()
    html = (
        f'<html lang="en"><body>Register view triggered. The path {path} was requested.</body></html>'
    )
    return HttpResponse(html)


def profile(request):
    path = request.get_full_path()
    html = f'<html lang="en"><body>Profile view triggered. The path {path} was'
    html += 'requested.</body></html>'
    return HttpResponse(html)
