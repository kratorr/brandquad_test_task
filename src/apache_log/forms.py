from django.forms import ModelForm


from .models import ApacheLog

class ApacheLogForm(ModelForm):
    class Meta:
        model = ApacheLog
        fields = ['ip_address', 'request_date', 'method', 'uri', 'response_size', 'response_code']