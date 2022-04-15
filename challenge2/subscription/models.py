from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class CustomerSubscription(models.Model):

    SUBSCRIPTION_STATE = (
        ("TRIAL", "trial"),
        ("SUBSCRIPTION", "subscription"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    state = models.CharField(
        max_length=64, choices=SUBSCRIPTION_STATE, null=False, blank=False
    )
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username
