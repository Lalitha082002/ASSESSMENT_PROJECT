from django.core.management.base import BaseCommand
from signals_demo.rectangle import Rectangle

class Command(BaseCommand):
    help = "Demonstrate Rectangle iteration."

    def handle(self, *args, **options):
        rectangle = Rectangle(length=10, width=5)
        self.stdout.write("Iterating over Rectangle(length=10, width=5):")
        for item in rectangle:
            self.stdout.write(str(item))
