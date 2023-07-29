import logging
from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import Ingredients


logger = logging.getLogger(__name__)
db_model = Ingredients
model_name = 'Ingredients'
file_name = 'ingredients.csv'
filepath = './test_data/' + file_name

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the {} data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables""".format(model_name)


class Command(BaseCommand):

    def handle(self, *args, **options):

        if db_model.objects.exists():
            logger.debug(f'{model_name} data already loaded...exiting.')
            logger.debug(ALREDY_LOADED_ERROR_MESSAGE)
            return

        logger.debug(f'Loading {model_name} data . . .')

        try:
            with open(filepath, mode="r", encoding="utf-8-sig") as csv_file:
                count = 1
                for row in DictReader(csv_file):
                    data = db_model(
                        # описание полей
                        id=count,
                        name=row['name'],
                        measurement_unit=row['measurement_unit']
                    )
                    count += 1
                    data.save()

            logger.debug(f'Saved {model_name} data')

        except Exception as e:
            logger.warning(e)
