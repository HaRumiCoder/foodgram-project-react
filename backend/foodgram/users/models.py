from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]


class Subscription(models.Model):
    subscribed_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriber",
        verbose_name="Подписан на",
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribed_to",
        verbose_name="Подписчик",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["subscribed_to", "subscriber"], name="unique_subscribe"
            )
        ]
