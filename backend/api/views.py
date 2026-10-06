from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .models import Crop, Season, FertilizerQualityChance
from .serializers import CropSerializer, SeasonSerializer, FertilizerQualityChanceSerializer

class APIRootView(APIView):
    def get(self, request):
        data = {
            'crops': reverse('crop-list', request=request),
            'seasons': reverse('season-list', request=request),
            'quality-probability': reverse('quality-list', request=request)
        }
        return Response(data)


class CropList(generics.ListAPIView):
    serializer_class = CropSerializer

    def get_queryset(self):
        queryset = Crop.objects.all()
        season = self.request.query_params.get('season')
        if season is not None:
            queryset = queryset.filter(season=season)
        return queryset
        

class CropDetail(generics.RetrieveAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer


class SeasonList(generics.ListAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer


class QualityList(generics.ListAPIView):
    queryset = FertilizerQualityChance.objects.all()
    serializer_class = FertilizerQualityChanceSerializer



