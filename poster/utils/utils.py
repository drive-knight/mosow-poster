import os
import requests
from django.core.files.base import ContentFile
from requests.exceptions import HTTPError
from requests.exceptions import RequestException

from poster.models import Place, Image


def create_place(data: dict):
    place, created = Place.objects.update_or_create(
     **{'title': data['title'],
        'latitude': data['coordinates']['lat'],
        'longitude': data['coordinates']['lng'],
        'short_description': data['description_short'],
        'long_description': data['description_long']},
    )
    if not created:
        print(f'Локация {place.title} уже есть в базе')
        return False
    for img_url in data['imgs']:
        img_name = os.path.basename(img_url)
        try:
            response = requests.get(img_url)
            response.raise_for_status()
            image_file = ContentFile(response.content, name=img_name)
            Image.objects.create(place=place, image=image_file)
        except RequestException as exc:
            print(f'Запрос к {img_url} не прошёл - {exc}')
            print(f'Создана запись о локации {place.title}')
    return True


def load_place_json(url):
    response = requests.get(url)
    response.raise_for_status()
    d_response = response.json()
    if 'error' in d_response:
        raise HTTPError(d_response['error'])
    try:
        create_place(d_response)
        print('Создана запись места')
    except RequestException as err:
        print(f'Запрос не удался - {err}')


def load_place_github(url):
    response = requests.get(url)
    response.raise_for_status()
    d_response = response.json()
    try:
        place_json_urls = [
            place['download_url'] for place in d_response
        ]
        place_d: list[dict] = [
            d_response for url in place_json_urls
        ]
        num_created = sum(
            create_place(json_data) for json_data in place_d
        )
        print(f'Записей о местах создано: {num_created} ')
    except RequestException as err:
        print(f'Запрос не удался - {err}')