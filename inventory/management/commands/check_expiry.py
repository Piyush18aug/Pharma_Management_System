from django.core.management.base import BaseCommand
from inventory.utils import check_and_create_alerts

class Command(BaseCommand):
    help = 'Checks for expiring medicines and generates alerts'

    def handle(self, *args, **options):
        self.stdout.write('Checking for expired medicines...')
        count = check_and_create_alerts()
        self.stdout.write(self.style.SUCCESS(f'Successfully checked expiry. Generated {count} new alerts.'))
