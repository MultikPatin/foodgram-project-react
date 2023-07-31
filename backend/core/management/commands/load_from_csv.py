from csv import DictReader

from django.core.management import BaseCommand


class LoadCSVData(BaseCommand):

    logger = None
    model = None
    file_path = None
    fields = []

    ALREDY_LOADED_ERROR_MESSAGE = """
    If you need to reload the model data from the CSV file,
    first delete the db.sqlite3 file to destroy the database.
    Then, run `python manage.py migrate` for a new empty
    database with tables"""

    def handle(self, *args, **options):

        model_name = self.model.__name__

        if self.model.objects.exists():
            self.logger.debug(
                f'{model_name} data already loaded...exiting.'
            )
            self.logger.debug(self.ALREDY_LOADED_ERROR_MESSAGE)
            return
        self.logger.debug(f'Loading {model_name} data . . .')
        try:
            with open(self.file_path,
                      mode='r',
                      encoding='utf-8-sig') as csv_file:
                count = 1
                models = []
                for row in DictReader(csv_file):
                    data = []
                    data.append(str(count))
                    for field in self.fields:
                        try:
                            data.append(row[field])
                        except KeyError as mes:
                            self.logger.warning(mes)
                    models.append(self.model(*data))
                    count += 1
                self.model.objects.bulk_create(models)

            self.logger.debug(f'Saved {model_name} data')

        except Exception as e:
            self.logger.warning(e)
