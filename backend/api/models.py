from django.db import models
from django.db.models import F, Value

SEASON_DAYS = 28

class Season(models.Model):
    SEASONS = [
        ("Spring", "Spring"),
        ("Summer", "Summer"),
        ("Fall", "Fall"),
        ("Winter", "Winter"),
    ]
    name = models.CharField(max_length=50, choices=SEASONS, unique=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.name


class CropQuerySet(models.QuerySet):
    def with_gold_per_day(self, price_multiplier=1.0):
        price = F('sell_price') * Value(price_multiplier)
        growing_days = F('growth_time') + ((F('max_harvest') - 1) * F('days_to_regrow'))

        return self.annotate(gold_per_day=
                             ((F('max_harvest') * price) - F('seed_price')) / growing_days)


class Crop(models.Model):
    name = models.CharField(max_length=100)
    season = models.ManyToManyField(Season, related_name="crops")
    special_location = models.CharField(max_length=100)
    growth_time = models.IntegerField()
    sell_price = models.IntegerField()
    seed_price = models.IntegerField(default=0)
    multiharvest = models.BooleanField(default=False, blank=True)
    days_to_regrow = models.IntegerField(default=0, blank=True)
    max_harvest = models.IntegerField(default=1, blank=True)

    objects = CropQuerySet.as_manager()

    class Meta:
        ordering = ['pk']
    
    def save(self, *args, **kwargs):
        if self.days_to_regrow != 0:
            self.max_harvest = (SEASON_DAYS - self.growth_time) // self.days_to_regrow + 1
        super().save()

    def __str__(self):
        return self.name


class Fertilizer(models.Model):
    TYPES = [
        ("Basic", "Basic"),
        ("Quality", "Quality"),
        ("Deluxe", "Deluxe"),
    ]
    type = models.CharField(max_length=10, choices=TYPES, unique=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.type


class FertilizerQualityChance(models.Model):
    fertilizer = models.ForeignKey(Fertilizer, on_delete=models.CASCADE, null=True)
    farming_level = models.IntegerField()
    regular_chance = models.IntegerField()
    silver_chance = models.IntegerField()
    gold_chance = models.IntegerField()
    iridium_chance = models.IntegerField()
    average_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{[self.fertilizer, self.farming_level, self.regular_chance, self.silver_chance, self.gold_chance, self.iridium_chance, self.average_price]}'
