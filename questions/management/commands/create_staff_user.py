from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create Staff User"

    def handle(self, *args, **kwargs):
        user = User.objects.create(username="admin", is_staff="True")
        user.set_password("admin")
        user.save()
