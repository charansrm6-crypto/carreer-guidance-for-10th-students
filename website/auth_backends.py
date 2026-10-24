from django.contrib.auth.backends import ModelBackend

from .models import Student


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, email=None, **kwargs):
        email = (email or username or kwargs.get("email") or "").strip()
        password = password or kwargs.get("password")
        if not email or not password:
            return None

        matches = list(Student.objects.filter(email__iexact=email)[:2])
        if len(matches) != 1:
            return None

        user = matches[0]
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        try:
            return Student.objects.get(pk=user_id)
        except Student.DoesNotExist:
            return None
