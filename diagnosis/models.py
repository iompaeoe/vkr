from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Doctor(models.Model):
    login =  models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    surname = models.CharField(max_length=100)
    name =  models.CharField(max_length=100)
    patronymic =models.CharField(max_length=100,blank=True,null=True)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False,blank=False, null=False)
    address = models.TextField()
    phone = models.CharField(max_length=11, blank=True,null=True)
    email =models.EmailField(max_length=254)
    specialty = models.ForeignKey('Specialty',on_delete=models.SET_NULL,null=True)
    def __str__(self):
        if self.patronymic == None:
            self.patronymic = '-'
        return '({0}) {1} {2} {3}'.format (self.login, self.surname,self.name,self.patronymic)

class Patient(models.Model):
    surname = models.CharField(max_length=100)
    name =  models.CharField(max_length=100)
    patronymic =models.CharField(max_length=100,blank=True,null=True)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False,blank=False, null=False)
    GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER, blank=True, default='m',)
    address = models.TextField()
    phone = models.CharField(max_length=11, blank=True,null=True)
    email =models.EmailField(max_length=254,blank=True,null=True)
    def __str__(self):
        if self.patronymic == None:
            self.patronymic = '-'
        age = timezone.now().year-self.date_of_birth.year
        return '({0}) {1} {2} {3} (Возраст: {4}, Пол: {5})'.format (self.id, self.surname,self.name,self.patronymic,age,self.gender)


class Question(models.Model):
    title = models.CharField(max_length=200, blank=False,null=False)
    text = models.TextField()
    def __str__(self):
        return '({0}) {1}'.format(self.id, self.title)

class Answer(models.Model):
    class Meta:
        unique_together = (('question','value'),)
    text=models.CharField(max_length=100)
    question = models.ForeignKey('Question',on_delete=models.CASCADE,null=False,blank=False)
    value = models.CharField(max_length=10,null=False,blank=False)
    def __str__(self):
        return '({0}) a:{1}; q:{2}; v:{3}'.format(self.id, self.text,self.question.id,self.value)


class Diagnosis(models.Model):
    patient = models.ForeignKey('Patient',on_delete=models.SET_NULL,null=True)
    doctor = models.ForeignKey('Doctor',on_delete=models.SET_NULL,null=True)
    diagnosis_date = models.DateTimeField(default=timezone.now)
    inquirer = models.ForeignKey('Inquirer',on_delete=models.SET_NULL,null=True)
    def __str__(self):
        return 'Diagnosis #{0}'.format(self.id)


class Survey(models.Model):
    class Meta:
        unique_together = (('diagnosis','question'),)
    diagnosis = models.ForeignKey('Diagnosis',on_delete=models.CASCADE,null=False,blank=False)
    question = models.ForeignKey('Question',on_delete=models.CASCADE,null=False,blank=False)
    answer = models.ForeignKey('Answer',on_delete=models.CASCADE,null = False,blank =False)
    def __str__(self):
        return '{0}: Вопрос "{1}"; Ответ "{2}"'.format(self.diagnosis,self.question.title,self.answer.text)

class Specialty(models.Model):
    name=models.CharField(max_length=200, blank=False,null=False)
    description = models.TextField()
    def __str__(self):
        return '({0}) {1}'.format(self.id, self.name)

class Inquirer(models.Model):
    name=models.CharField(max_length=200, blank=False,null=False)
    description = models.TextField()
    ANN_model = models.FileField(max_length=None)
    def __str__(self):
        return '({0}) {1}'.format(self.id, self.name)

class SpecialityInquirer(models.Model):
    class Meta:
        unique_together = (('specialty','inquirer'),)
    specialty = models.ForeignKey('Specialty',on_delete=models.CASCADE,null=False,blank=False)
    inquirer = models.ForeignKey('Inquirer',on_delete=models.CASCADE,null=False,blank=False)

class InquirerQuestion(models.Model):
    class Meta:
        unique_together = (('inquirer','question'),)
    inquirer = models.ForeignKey('Inquirer',on_delete=models.CASCADE,null=False,blank=False)
    question = models.ForeignKey('Question',on_delete=models.CASCADE,null=False,blank=False)
    def __str__(self):
        return 'Опросник {0}; Вопрос: {1}'.format(self.inquirer.name,self.question.title)

class Result(models.Model):
    name = models.CharField(max_length=200,blank=False,null=False)
    description = models.TextField()
    code = models.IntegerField(blank=False,null=False)
    def __str__(self):
        return 'Диагноз: {}'.format(self.name)

class DiagnosisResult(models.Model):
    class Meta:
        unique_together = (('diagnosis','result'),)
    diagnosis = models.ForeignKey('Diagnosis',on_delete=models.CASCADE,null=False,blank=False)
    result = models.ForeignKey('Result',on_delete=models.CASCADE,null=False,blank=False)
    def __str__(self):
        return 'Для диагностики {0} {1}'.format(self.diagnosis.id, self.result) 