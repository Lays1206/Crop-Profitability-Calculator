from rest_framework import serializers
from .models import Crop, Season, Fertilizer, FertilizerQualityChance


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'


class CropSerializer(serializers.ModelSerializer):
    season = SeasonSerializer(many=True)
   
    class Meta:
        model = Crop
        fields = ['id','name','season','special_location', 'growth_time',
                  'sell_price', 'seed_price', 'multiharvest', 'days_to_regrow', 'max_harvest'] 


class CropQuerySetSerializer(serializers.ModelSerializer):
    gold_per_day = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Crop
        fields = ['id','name','sell_price','seed_price','gold_per_day']


class FertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertilizer
        fields = '__all__'


class FertilizerQualityChanceSerializer(serializers.ModelSerializer):
    fertilizer = FertilizerSerializer(read_only=True)
   
    class Meta:
        model = FertilizerQualityChance
        fields = '__all__'
