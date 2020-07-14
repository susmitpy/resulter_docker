from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User,Group
from django.contrib.auth.models import Permission


class Command(BaseCommand):

    def handle(self, *args, **options):
       print("Initial Auth Set Up")

       if not Group.objects.filter(name="admin").exists() :
           admin_group = Group.objects.create(name="admin")
           Group.objects.create(name="administration")
           Group.objects.create(name="faculty")

       perms_list = ["Can add subject","Can view subject", "Can add division", "Can view division", "Can delete subject", "Can delete division"]
       permissions = Permission.objects.filter(name__in=perms_list)
       admin_group = Group.objects.get(name="admin")
       user = User.objects.create(username="admin")
       user.set_password("1234")
       user.groups.add(admin_group)
       user.is_staff = True
       for permission in permissions:
           user.user_permissions.add(permission)
       user.save()



       print("Created Groups and admin user")
