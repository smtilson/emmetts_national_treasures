from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    #path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("set_handle", views.set_handle, name="set_handle"),
    path("user_page", views.user_page, name="user_page"),
    path("add_friend", views.add_friend, name="add_friend"), 
    #or is it better to pass the form data in the url?
]