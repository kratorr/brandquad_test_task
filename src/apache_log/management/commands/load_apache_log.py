import requests
import apache_log_parser


from django.core.management.base import BaseCommand


from apache_log.models import ApacheLog
from apache_log.forms import ApacheLogForm


CHUNK_SIZE = 5000


class Command(BaseCommand):
    help = 'Upload apache log to DB'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        self.stdout.write('Start download file')

        line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b")

        with requests.get(options['url'], stream=True) as response:
            response.raise_for_status()
            log_to_insert = []
            for log_line in response.iter_lines(chunk_size=CHUNK_SIZE):
                if log_line:
                    try:
                        parsed_log = line_parser(log_line.decode('utf-8'))
                    except apache_log_parser.LineDoesntMatchException:
                        continue
                    data = {
                        'ip_address': parsed_log['remote_host'],
                        'request_date': parsed_log['time_received_tz_datetimeobj'],
                        'response_code': parsed_log['status'],
                        'response_size': 0 if parsed_log['response_bytes_clf'] == '-' else parsed_log['response_bytes_clf'],
                        'uri': parsed_log['request_url'],
                        'method': parsed_log['request_method']
                    }
                    if ApacheLogForm(data=data).is_valid():
                        log_to_insert.append(ApacheLog(**data))
                if len(log_to_insert) == CHUNK_SIZE:
                    ApacheLog.objects.bulk_create(log_to_insert)
                    self.stdout.write('Insert chunk into DB')
                    log_to_insert = []

            if log_to_insert:
                ApacheLog.objects.bulk_create(log_to_insert)
                self.stdout.write('Insert chunk into DB')
      
        self.stdout.write(self.style.SUCCESS('Successfully upload apache log'))
