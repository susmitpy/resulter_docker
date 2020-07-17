from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User,Group
from django.contrib.auth.models import Permission


class Command(BaseCommand):

    def handle(self, *args, **options):
       print("Initial Auth Set Up")

       if not Group.objects.filter(name="admin").exists() :
           admin_group = Group.objects.create(name="admin")
           perms_list = ["Can add subject","Can view subject", "Can add division", "Can view division", "Can delete subject", "Can delete division"]
           permissions = Permission.objects.filter(name__in=perms_list)
           for permission in permissions:
               admin_group.permissions.add(permission)
           admin_group.save()
           Group.objects.create(name="administration")
           Group.objects.create(name="faculty")

       if not User.objects.filter(username="admin").exists():

           admin_group = Group.objects.get(name="admin")
           user = User.objects.create(username="admin")
           user.set_password("1234")
           user.is_staff = True
           user.groups.add(admin_group)

           user.save()



       print("Created Groups and admin user")
