# subscription/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="subscription-home"),
    path("config/", views.stripe_config),
    path("create-checkout-session/", views.create_checkout_session),
    path("success/", views.success),
    path("cancel/", views.cancel),
    # path('webhook/', views.stripe_webhook),
    path(
        "register/<slug:state>", views.create_user, name="django_registration_register"
    ),
]
