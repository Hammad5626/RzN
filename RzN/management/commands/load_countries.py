import json
from django.core.management.base import BaseCommand
from RzN.models import Country, Timezone

class Command(BaseCommand):
    help = "Load countries and timezones from JSON"

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help="Path to countries JSON file")

    def handle(self, *args, **options):
        file_path = options['file']

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for country_data in data:
            # Create country
            country, created = Country.objects.update_or_create(
                name=country_data['name'],
                defaults={'flag': country_data.get('emoji', '')}
            )

            # Delete old timezones if they exist
            country.timezones.all().delete()

            # Add all timezones for this country
            for tz in country_data.get('timezones', []):
                Timezone.objects.create(
                    country=country,
                    zone_name=tz['zoneName'],
                    gmt_offset=tz['gmtOffset'],
                    gmt_offset_name=tz['gmtOffsetName']
                )

        self.stdout.write(self.style.SUCCESS('Countries and timezones loaded successfully!'))
