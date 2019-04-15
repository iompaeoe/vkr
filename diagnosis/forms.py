from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime
class DiagnosisForm(forms.Form):
    doctor = forms.IntegerField()
    



