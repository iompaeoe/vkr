# модуль, предназначенный для генерации документа на 
# основе заранее подготовленного шаблона
from __future__ import print_function
import io
from mailmerge import MailMerge
from datetime import date
# -*- codecs: utf-8 -*-
##import codecs

# метод, предназначеный для генерации
# документа на основе шаблона. 
# входными данными являютя файл шаблона 
# и массив данных для заполнения
# возвращает заполненный данными документ
# в виде набора байтов 
def download(template,data):
    document = MailMerge(template)
 
    document.merge(
    	patients_surname=data['patients_surname'],
    	patients_name=data['patients_name'],
    	patients_patronymic=data['patients_patronymic'],
    	patients_date_of_birth=data['patients_date_of_birth'],
        diagnosis_date=data['diagnosis_date'],
    	diagnosis_results=data['diagnosis_results']
    	)
    f = io.BytesIO()
    document.write(f)

    return f
