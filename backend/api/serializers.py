from rest_framework import serializers
from .models import Crop, Season, Fertilizer, FertilizerQualityChance
from .utils.calculate_quality import calculate_quality


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'


class CropSerializer(serializers.ModelSerializer):
    season = SeasonSerializer(many=True)
    quality_probability = serializers.SerializerMethodField()

    class Meta:
        model = Crop
        fields = ['id','name','season','special_location', 'quality_probability','growth_time',
                  'sell_price', 'seed_price', 'multiharvest', 'days_to_regrow', 'max_harvest']
    def get_quality_probability(self, obj):
        request = self.context.get('request')
        if request:
            farming_level = request.query_params.get('level')
            fertilizer = request.query_params.get('fertilizer')
        return calculate_quality(fertilizer, farming_level) 


class FertilizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fertilizer
        fields = '__all__'


class FertilizerQualityChanceSerializer(serializers.ModelSerializer):
    fertilizer = FertilizerSerializer(read_only=True)
    class Meta:
        model = FertilizerQualityChance
        fields = '__all__'
