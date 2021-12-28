from django.core.management import BaseCommand

from poster.utils import load_place_json


class Command(BaseCommand):
    help = 'Добавить место на карту из json файла'

    def add_arguments(self, parser):
        parser.add_argument('--json_file')

    def handle(self, *args, **options):
        load_place_json(options['json_file'])