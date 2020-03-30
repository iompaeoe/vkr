# Тема ВКР: разработка программного обеспечения информационной системы для постановки диагноза пациентам госпиталя
# Студент: Бабенко С.В., направление 09.05.01, группа 4414
# Руководитель ВКР: Бубнов С.А. к.ф-м.н., доцент кафедры ВПМ
# Средства разработки: Python 3.7.2, Django 2.1.7, Bootstrap 4, SQLite 3.27.2, Visual Studio Code 1.31.1, Windows 10
# Дата разработки: 31.05.2019 г.

# Модуль используемых моделей. Классы, содержащиеся в нем, являются сущностями базы данных.
# С помощью моделей происходит взаимодействие с базой данных.

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
# функция,возвращающая имя пользователя "deleted",
# используемое для замены в таблицах удаленног пользователя
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]
# класс врача-специалиста, являющийся сущностью БД
# содержит логин и пароль, предназначенные для входа в систему,
# фамилию, имя, отчество, дату рождения, адрес, телефон, эл.почту,
# специальность, которая связана с сущностью "Специальность"
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
    avatar = models.ImageField(upload_to='images/',default='images/no-profile.jpg')
    # Возвращает текстовое описание врача.
    # Используется, если необходимо отобразить краткую информацию о враче
    def __str__(self):
        if self.patronymic == None:
            self.patronymic = '-'
        return '({0}) {1} {2} {3}'.format (self.login, self.surname,self.name,self.patronymic)
# класс пациента, являющийся сущностью БД
# сожержит фамилия, имя, отчество,дату рождения, пол,
# адрес, телефон, эл.почту
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
    # метод, возвращающий текстовое описание пациента
    # Используется, если необходимо отобразить краткую информацию о пациенте
    def __str__(self):
        if self.patronymic == None:
            self.patronymic = '-'
        age = timezone.now().year-self.date_of_birth.year
        return '({0}) {1} {2} {3} (Возраст: {4}, Пол: {5})'.format (self.id, self.surname,self.name,self.patronymic,age,self.gender)
# класс вопроса, являющийся сущностью БД
# сожержит заголовок и текст
class Question(models.Model):
    title = models.CharField(max_length=200, blank=False,null=False)
    text = models.TextField()
    # метод, возвращающий текстовое описание вопроса в краткой форме
    # Используется, если необходимо отобразить краткую информацию о вопросе
    def __str__(self):
        return '({0}) {1}'.format(self.id, self.title)
# класс ответа, являющийся сущностью БД
# сожержит мета-класс для обеспечения совместной уникальности
# полей "вопрос" и "значение",
# текст ответа, вопрос, с которым он связан,
# значение, предназначенное для дальньнейшей обработки
class Answer(models.Model):
    class Meta:
        unique_together = (('question','value'),)
    text=models.CharField(max_length=100)
    question = models.ForeignKey('Question',on_delete=models.CASCADE,null=False,blank=False)
    value = models.CharField(max_length=10,null=False,blank=False)
    # возвращает краткое текстовое описание ответа
    # Используется, если необходимо отобразить краткую информацию о вопросе
    def __str__(self):
        return '({0}) a:{1}; q:{2}; v:{3}'.format(self.id, self.text,self.question.id,self.value)

# класс диагностики, являющийся сущностью БД
# содержит связанных с ней пациента, врача, опросника и дату/время проведения
class Diagnosis(models.Model):
    patient = models.ForeignKey('Patient',on_delete=models.SET_NULL,null=True)
    doctor = models.ForeignKey('Doctor',on_delete=models.SET_NULL,null=True)
    diagnosis_date = models.DateTimeField(default=timezone.now)
    inquirer = models.ForeignKey('Inquirer',on_delete=models.SET_NULL,null=True)
     # возвращает краткое текстовое описание диагностики
    # Используется, если необходимо отобразить краткую информацию о ней
    def __str__(self):
        return 'Diagnosis #{0}'.format(self.id)

# класс собранных данных о пациенте, являющийся сущностью БД
# содержит мета-класс, обеспечивающий совместную уникальность диагностики и вопроса,
# поля диагностики, связанной с ним, вопрос, связанный с ним, и данный пациентом ответ
class Survey(models.Model):
    class Meta:
        unique_together = (('diagnosis','question'),)
    diagnosis = models.ForeignKey('Diagnosis',on_delete=models.CASCADE,null=False,blank=False)
    question = models.ForeignKey('Question',on_delete=models.CASCADE,null=False,blank=False)
    answer = models.ForeignKey('Answer',on_delete=models.CASCADE,null = False,blank =False)
    #возвращает краткое текстовое описание пары вопрос-данный ответ
    # Используется, если необходимо отобразить краткую информацию о нем
    def __str__(self):
        return '{0}: Вопрос "{1}"; Ответ "{2}"'.format(self.diagnosis,self.question.title,self.answer.text)
# класс врачебной специальности, являющийся сущностью БД
# имеет название и описание
class Specialty(models.Model):
    name=models.CharField(max_length=200, blank=False,null=False)
    description = models.TextField()
    # возвращает краткое текстовое описание специальности
    # Используется при необходимости отображения краткой информации
    def __str__(self):
        return '({0}) {1}'.format(self.id, self.name)
# класс опросника, являющийся сущностью БД
# имеет название, описание, внешний модуль-анализатор, шаблон медицинского заключения
# и булева поля, определяющего, анализируется ли результаты с помощью методов
# машинного обучения
class Inquirer(models.Model):
    name=models.CharField(max_length=200, blank=False,null=False)
    description = models.TextField()
    solver = models.FileField(max_length=None)
    medical_report_template = models.FileField (max_length=None,blank=True,null=True)
    is_ann = models.BooleanField(default = False)
    # возвращает краткое текстовое описание опросника
    def __str__(self):
        return '({0}) {1}'.format(self.id, self.name)
# класс, связывающий специальность и опросника
# имеет мета-класс, обеспечивающий уникальность пары специальность-опросник
class SpecialityInquirer(models.Model):
    class Meta:
        unique_together = (('specialty','inquirer'),)
    specialty = models.ForeignKey('Specialty',on_delete=models.CASCADE,null=False,blank=False)
    inquirer = models.ForeignKey('Inquirer',on_delete=models.CASCADE,null=False,blank=False)
# класс связывающий опросник и вопрос
# имеет мета-класс, обеспечивающий уникальность пары полей опросник-вопрос
class InquirerQuestion(models.Model):
    class Meta:
        unique_together = (('inquirer','question'),)
    inquirer = models.ForeignKey('Inquirer',on_delete=models.CASCADE,null=False,blank=False)
    question = models.ForeignKey('Question',on_delete=models.CASCADE,null=False,blank=False)
    # метод, выводящий краткую текстовую информацию о сущности
    def __str__(self):
        return 'Опросник {0}; Вопрос: {1}'.format(self.inquirer.name,self.question.title)
# класс всех возможных результатов обследования, являющийся сущностью БД
# имеет наименование, описание, шифр
class Result(models.Model):
    name = models.CharField(max_length=200,blank=False,null=False)
    description = models.TextField()
    code = models.CharField(max_length=50,blank=False,null=False,unique=True)
    # метод, выводящий краткую текстовую информацию о сущности
    def __str__(self):
        return 'Диагноз: {}'.format(self.name)
# класс, связывающий диагностику с полученным результатом
# содержит мета-класс, обеспечивающий уникальность пары диагностика-результат
class DiagnosisResult(models.Model):
    class Meta:
        unique_together = (('diagnosis','result'),)
    diagnosis = models.ForeignKey('Diagnosis',on_delete=models.CASCADE,null=False,blank=False)
    result = models.ForeignKey('Result',on_delete=models.CASCADE,null=False,blank=False)
    # метод, выводящий краткую текстовую информацию о сущности
    def __str__(self):
        return 'Для диагностики {0} {1}'.format(self.diagnosis.id, self.result) 