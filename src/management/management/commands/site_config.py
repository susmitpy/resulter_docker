from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
my_site = Site.objects.get(pk=1)


class Command(BaseCommand):

    def handle(self, *args, **options):
       print("Site Configuration")
       my_site = Site.objects.get(pk=1)
       my_site.domain="ec2-52-66-243-195.ap-south-1.compute.amazonaws.com"
       my_site.name = "resulter"
       my_site.save()
