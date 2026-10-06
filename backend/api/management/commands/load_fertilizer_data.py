import csv
from django.core.management.base import BaseCommand, CommandError
from api.models import Fertilizer, FertilizerQualityChance

# Handles migrations/data loading for fertilizer and fertilizer quality chance models
class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('api/data/fertilizer_quality.csv') as file:
            fertilizer_reader = csv.DictReader(file)

            for row in fertilizer_reader:
                fertilizer = None
                if row["fertilizer"].strip():
                    fertilizer, _ = Fertilizer.objects.get_or_create(type=row["fertilizer"].strip())

                FertilizerQualityChance.objects.update_or_create(
                    fertilizer = fertilizer,
                    farming_level = int(row["farming_level"].strip()),
                    defaults={
                        "regular_chance": int(row["regular_chance"].strip()),
                        "silver_chance": int(row["silver_chance"].strip()),
                        "gold_chance": int(row["gold_chance"].strip()),
                        "iridium_chance": int(row["iridium_chance"].strip()),
                        "average_price": float(row["average_price"].strip()),
                    }        
                )