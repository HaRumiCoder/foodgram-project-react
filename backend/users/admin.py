from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscription

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    list_filter = ("username", "email")


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "subscribed_to")
    list_filter = ("subscriber", "subscribed_to")


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
