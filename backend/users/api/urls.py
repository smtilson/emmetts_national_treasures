from django.urls import path, include
from .views import UserViewSet, SignupView, LoginView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    # or is it better to pass the form data in the url?
]
