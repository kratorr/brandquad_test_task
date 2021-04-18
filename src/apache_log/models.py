from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class ApacheLog(models.Model):
    HTTP_METHODS = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('HEAD', 'HEAD'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
        ('TRACE', 'TRACE'),
        ('CONNECT', 'CONNECT')
    ]

    #ip_address = models.GenericIPAddressField(db_index=True, verbose_name='ip адрес')  #GenericIPAddressField не сработал, в логе попадаюстя значения "5.176.255.173.unassigned.as54203.net"
    ip_address = models.CharField(max_length=50, db_index=True, verbose_name='ip адрес')
    request_date = models.DateTimeField(verbose_name='дата и время запроса')
    method = models.CharField(max_length=7, choices=HTTP_METHODS, verbose_name='метод', db_index=True)
    uri = models.TextField(verbose_name='запрос')
    response_size = models.PositiveIntegerField(verbose_name='размер ответа')
    response_code = models.PositiveIntegerField(validators=[MinValueValidator(100), MaxValueValidator(526)],
                                                verbose_name='код ответа', db_index=True)

    class Meta:
        ordering = ['-request_date']
