from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .models import Crop, Season, FertilizerQualityChance
from .serializers import CropSerializer, CropQuerySetSerializer, SeasonSerializer, FertilizerQualityChanceSerializer

class APIRootView(APIView):
    def get(self, request):
        data = {
            'crops': reverse('crop-list', request=request),
            'seasons': reverse('season-list', request=request),
            'quality-probability': reverse('quality-list', request=request),
            'gold-per-day': reverse('gold-per-day', request=request),
        }
        return Response(data)


class CropList(generics.ListAPIView):
    serializer_class = CropSerializer

    def get_queryset(self):
        queryset = Crop.objects.all()
        season = self.request.query_params.get('season')
        if season is not None:
            queryset = queryset.filter(season__name=season.capitalize())
        return queryset
        

class CropDetail(generics.RetrieveAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer


class GoldPerDayList(generics.ListAPIView):
    serializer_class = CropQuerySetSerializer

    def get_queryset(self):
        farming_level = self.request.query_params.get('farming_level', 0)
        try:
            farming_level = int(farming_level)
        except ValueError:
            raise ValidationError({"detail": f"Invalid farming_level '{farming_level}'; must be an integer from 0-14."})
        
        fertilizer_type = self.request.query_params.get('fertilizer')

        try:
            quality = FertilizerQualityChance.objects.get(fertilizer__type=fertilizer_type, farming_level=farming_level)
        except FertilizerQualityChance.DoesNotExist:
            raise ValidationError({"detail": f"Invalid farming_level '{farming_level}' or "
                                             f"fertilizer '{fertilizer_type}'. farming_level must be 0-14 "
                                             f"and fertilizer must be Basic, Quality, or Deluxe."})

        queryset = Crop.objects.with_gold_per_day(float(quality.average_price))
        return queryset.order_by("-gold_per_day")


class SeasonList(generics.ListAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer


class QualityList(generics.ListAPIView):
    queryset = FertilizerQualityChance.objects.all()
    serializer_class = FertilizerQualityChanceSerializer



