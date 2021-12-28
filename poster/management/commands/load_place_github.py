from urllib.parse import urlparse
from django.core.management import BaseCommand
from poster.utils import load_place_github


class Command(BaseCommand):
    help = 'Добавить место на карту из Github репозитория'

    def add_arguments(self, parser):
        parser.add_argument('--github_url')

    def handle(self, *args, **options):
        path_folder = urlparse(options['github_url']).path
        owner, rep, *_, folder = list(filter(None, path_folder.split('/')))
        download_url = f'https://api.github.com/repos/{owner}/{rep}/contents/{folder}'
        load_place_github(download_url)


