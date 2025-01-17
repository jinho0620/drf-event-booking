from django.urls import include, path, re_path
from . import views

urlpatterns = [
    # path("", include("dj_rest_auth.urls")),
    path("accounts/", include("allauth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("google/", views.GoogleLogin.as_view(), name="google_login"),
    path(
        "google/callback/",
        views.GoogleLoginCallback.as_view(),
        name="google_login_callback",
    ),
]
