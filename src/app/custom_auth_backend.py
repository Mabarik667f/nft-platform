from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class CustomAuthBackend(BaseBackend):

    def authenticate(self, request, **kwargs):
        try:
            return User.objects.get()
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
