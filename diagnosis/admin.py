from django.contrib import admin
from .models import Doctor, Patient, Question, Answer, Diagnosis, Survey
# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Diagnosis)
admin.site.register(Survey)
