from django.apps import AppConfig

from django.contrib.auth import get_user_model
User = get_user_model()

class UsersConfig(AppConfig):
    name = 'users'
