# модуль предназначен для обработки поступающих запросов от клиента
# с помощью соответствующих функций

from django.shortcuts import render, get_object_or_404
from .models import Patient, Diagnosis, Question, Answer, Doctor, Survey, Inquirer, SpecialityInquirer, InquirerQuestion, Result, DiagnosisResult
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .forms import DiagnosisForm
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from .neuro import predicate
from .solver import import_source
from .med_report_handler import download
import transliterate
import pickle
import sklearn
from sklearn.externals import joblib
import io
# метод, возвращающий главную страницу
# для выполнения требуется авторизация пользователя в системе
@login_required
def main(request):
    return render(request, 'diagnosis/main.html', {})
# метод, возвращающий страницу списка пациентов
# передает в контекст список всех пациентов
# для выполнения требуется авторизация пользователя в системе
@login_required
def patients_list(request):
    patients= Patient.objects.all()
    return render(request, 'diagnosis/patients.html', {'patients':patients})
# метод, возвращающий страницу информации о пациенте
# передает в контекст информацию о пациенте
# для выполнения требуется авторизация пользователя в системе
@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'diagnosis/patient_detail.html', {'patient': patient})
# метод, возвращающий страницу информации о диагностике
# передает в контекст информацию о диагностике, включая собранные
# во время обследования данные о пациенте 
# для выполнения требуется авторизация пользователя в системе
@login_required
def diagnosis_detail(request,pk):
    diagnosis = get_object_or_404(Diagnosis, pk=pk)
    surveys = Survey.objects.filter(diagnosis=diagnosis)
    diagnosis_result = DiagnosisResult.objects.filter(diagnosis=diagnosis)
    return render(request, 'diagnosis/diagnosis_detail.html', {'diagnosis': diagnosis,'surveys':surveys,'results':diagnosis_result,})
# метод, возвращающий страницу диагностики
# передает в контекст информацию о диагностике, пациентах, вопросы с соответствующими ответами, опросник
# для выполнения требуется наличие прав на добавление диагноза
# для выполнения требуется авторизация пользователя в системе
@permission_required('diagnosis.add_diagnosis')
@login_required
def diagnosis_new(request,pk):
    form = DiagnosisForm()
    patients = Patient.objects.all()
    answers = Answer.objects.all()
    inquirer = get_object_or_404(Inquirer,pk=pk)
    InquirerQuestions=InquirerQuestion.objects.filter(inquirer=inquirer)
    questions = []
    for iq in InquirerQuestions:
        questions.append(iq.question)
    context = {
        'form': form,
        'patients':patients,
        'questions':questions,
        'answers':answers,
        'inquirer':inquirer,
    }
    return render(request, 'diagnosis/diagnosis_new.html', context)
# метод, выполняющий анализ и сохранение результатов обследования
# возвращает страницу с информацией о диагностике
# для выполнения требуется наличие прав на добавление диагноза
# для выполнения требуется авторизация пользователя в системе
@permission_required('diagnosis.add_diagnosis')
@login_required
def save_diagnosis(request,pk):
    with transaction.atomic():
        patient_code = request.POST.get('patient')
        patient = get_object_or_404(Patient,id=patient_code)
        doctor_code = request.POST.get('doctor')
        user = get_object_or_404(User,username=doctor_code)
        doctor = get_object_or_404(Doctor,login = user)
        diagnosis_date = timezone.now()
        inquirer= get_object_or_404(Inquirer,id=pk)
        diagnosis = Diagnosis(patient=patient,doctor=doctor,diagnosis_date=diagnosis_date, inquirer=inquirer)
        diagnosis.save()
        questions = []
        answer_values=[]
        InquirerQuestions=InquirerQuestion.objects.filter(inquirer=inquirer)
        for iq in InquirerQuestions:
            questions.append(iq.question)
        for question in questions:
            answer_code = request.POST.get('answerRadioForQuestion{0}'.format(question.id))
            answer = get_object_or_404(Answer,id=answer_code)
            survey = Survey(diagnosis=diagnosis, question=question, answer=answer)
            answer_values.append(int(answer.value))
            survey.save()
        answer_values.append(int(timezone.now().year-patient.date_of_birth.year))
        if inquirer.is_ann:
            model = joblib.load(inquirer.solver)
            result_code = predicate(answer_values,model)
        else:
            module = import_source(inquirer.solver)
            result_code=module.analysis(answer_values)
            print("--->",result_code)
        for r in result_code:
            diagnosis_result = get_object_or_404(Result,code=r)
            diagnosis_result = DiagnosisResult(diagnosis=diagnosis,result=diagnosis_result)
            diagnosis_result.save()
        print (diagnosis_result)
    return diagnosis_detail(request,pk=diagnosis.id)
# метод, предназначенный для выбора опросника
# возвращает страницу выбора опросников
# для выполнения требуется наличие прав на добавление диагноза
# для выполнения требуется авторизация пользователя в системе
@login_required
@permission_required('diagnosis.add_diagnosis')
def select_inquirer(request):
    user = request.user
    doctor = get_object_or_404(Doctor,login = user)
    specialty = doctor.specialty_id
    speciality_inquirers = SpecialityInquirer.objects.filter(specialty=specialty)
    return render(request, 'diagnosis/select_inquirer.html', {'inquirers': speciality_inquirers})
# метод, выполняющий генерацию файла на основе заранее загруженного шаблона
# возвращает сгенерированный документ
# для выполнения требуется наличие прав на добавление диагноза
# для выполнения требуется авторизация пользователя в системе
@login_required
@permission_required('diagnosis.add_diagnosis')
def download_diagnosis_result(request,pk):
    diagnosis = get_object_or_404(Diagnosis,id=pk)
    diagnosis_results=DiagnosisResult.objects.filter(diagnosis=diagnosis)
    patient = diagnosis.patient
    template=diagnosis.inquirer.medical_report_template
    d_r=''
    for r in diagnosis_results:
        d_r=d_r+r.result.name+'\n'+r.result.description+'\n'+'\n'
    data = {
        'patients_surname': patient.surname,
        'patients_name':patient.name,
        'patients_patronymic':patient.patronymic,
        'patients_date_of_birth': '{0} (Полных лет: {1})'.format(patient.date_of_birth,diagnosis.diagnosis_date.year-patient.date_of_birth.year),
        'diagnosis_date':'{0}'.format(diagnosis.diagnosis_date),
        'diagnosis_results':d_r,
    }
    filename='{0}_{1}_{2}-{3}-{4}'.format(diagnosis.inquirer.name,patient.surname,diagnosis.diagnosis_date.day,diagnosis.diagnosis_date.month,diagnosis.diagnosis_date.year)
    filename = transliterate.translit(filename,reversed=True)
    med_report_file=download(template,data)
    length = med_report_file.tell()
    med_report_file.seek(0)
    response = HttpResponse(
        med_report_file.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
         )
    response['Content-Disposition'] = 'attachment; filename={0}.docx'.format(filename)
    response['Content-Length'] = length
    return response

@login_required
@permission_required('diagnosis.add_diagnosis')
def profile(request,pk):
    user = get_object_or_404(User,username=pk)
    doctor = get_object_or_404(Doctor,login = user)
    print('suc')
    context = {
        'doctor':doctor,
    }
    return render(request,'diagnosis/profile.html',context)
    