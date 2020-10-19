from django.contrib.gis.geos import GEOSGeometry
from rest_framework.filters import BaseFilterBackend


class DistanceToPointFilter(BaseFilterBackend):
    """
    Distance To Point Filter used for filter get request responses on lat lon and radius level.
    """
    def filter_queryset(self, request, queryset, view):
        _lat = request.query_params.get('lat', None)
        _long = request.query_params.get('long', None)
        _radius = request.query_params.get('radius', 1000)
        if not _lat or not _long:
            return queryset
        point = GEOSGeometry(f'POINT({_long} {_lat})')
        query = queryset.filter(point__dwithin=(point, _radius))
        return query
