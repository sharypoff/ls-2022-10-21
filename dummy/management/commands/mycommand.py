from django.core.management.base import BaseCommand
from dummy.models import SimpleLamp


class Command(BaseCommand):
    def handle(self, *args, **options):
        simplelamps = SimpleLamp.objects.all()
        print(list(simplelamps))
