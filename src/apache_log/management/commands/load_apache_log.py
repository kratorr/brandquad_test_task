import requests
import apache_log_parser


from django.core.management.base import BaseCommand

from apache_log.models import ApacheLog


class Command(BaseCommand):
    help = 'Upload apache log to DB'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        self.stdout.write('Start download file')
        response = requests.get(options['url'])
        response.raise_for_status()

        line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b")
        log_to_insert = []

        for log_line in response.content.decode('utf-8').splitlines():
            if log_line:
                parsed_log = line_parser(log_line)
                log_to_insert.append(ApacheLog(
                    ip_address=parsed_log['remote_host'],
                    request_date=parsed_log['time_received_tz_datetimeobj'],
                    response_code=parsed_log['status'],
                    response_size=0 if parsed_log['response_bytes_clf'] == '-' else parsed_log['response_bytes_clf'],
                    uri=parsed_log['request_url'],
                    method=parsed_log['request_method']
                    )
                )
        self.stdout.write('Start upload to DB')
        ApacheLog.objects.bulk_create(log_to_insert)

        self.stdout.write(self.style.SUCCESS('Successfully upload apache log'))