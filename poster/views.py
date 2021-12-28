from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Place


def main_page(request):
    places = {
        'type': 'FeatureCollection',
        'features': [{'type': 'Feature',
                      'geometry': {'type': 'Point',
                                   'coordinates': [place.lng, place.lat]
                                   },
                      'properties': {'title': place.title,
                                     'placeId': place.pk,
                                     'detailsUrl': reverse('place', args={'place_id': place.slug})
                                     }
                      }
                     for place in Place.objects.all()]
    }

    return render(request, 'index.html', context={'places': places})


def place_detail(request, slug):
    place = get_object_or_404(Place, slug=slug)
    place_details = {
        'title': place.title,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'imgs': [image.image.url for image in place.images.all()],
        'coordinates': {
            'lng': place.lng,
            'lat': place.lat
        },
    }
    return JsonResponse(place_details, json_dumps_params={'ensure_ascii': False, 'indent': 2})