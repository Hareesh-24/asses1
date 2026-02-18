import json
import math
from django.core.management.base import BaseCommand
from recipe_list.models import Recipe


def clean_nan(value):
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, str) and value.strip().lower() == 'nan':
        return None
    return value


class Command(BaseCommand):
    help = 'Load recipes from a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            default='recipes.json',
            help='Path to JSON file (default: recipes.json)'
        )

    def handle(self, *args, **options):
        filepath = options['file']

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {filepath}"))
            return

        created = skipped = 0

        for item in data.values():
            title = item.get('title', '').strip() if item.get('title') else ''
            if not title:
                skipped += 1
                continue

            recipe, was_created = Recipe.objects.get_or_create(
                title=title,
                defaults={
                    'cuisine':     item.get('cuisine', ''),
                    'rating':      clean_nan(item.get('rating')),
                    'prep_time':   clean_nan(item.get('prep_time')),
                    'cook_time':   clean_nan(item.get('cook_time')),
                    'total_time':  clean_nan(item.get('total_time')),
                    'description': item.get('description', ''),
                    'nutrients':   item.get('nutrients') or None,
                    'serves':      item.get('serves', ''),
                }
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"Done! Created: {created}, Skipped (duplicates): {skipped}"
        ))