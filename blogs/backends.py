from django.contrib.auth.backends import BaseBackend, UserModel
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

USER = get_user_model()


class CustomEmailBackend:

    def authenticate(self, request, username, password, **kwargs):
        try:
            user = USER.objects.get(email=username)
            success = user.check_password(password)
            if success:
                return user
        except USER.DoesNotExist:
            pass
        return None

    def get_user(self, id):
        try:
            return USER.objects.get(pk=id)
        except:
            return None
