from django.shortcuts import render, get_object_or_404
from .models import Patient, Diagnosis, Question, Answer, Doctor, Survey, Inquirer, SpecialityInquirer, InquirerQuestion
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import DiagnosisForm
from django.db import transaction
from django.conf import settings
from django.utils import timezone
from .neuro import predicate
import sklearn
from sklearn.externals import joblib

@login_required
def main(request):
    return render(request, 'diagnosis/main.html', {})

@login_required
def patients_list(request):
    patients= Patient.objects.all()
    return render(request, 'diagnosis/patients.html', {'patients':patients})

@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'diagnosis/patient_detail.html', {'patient': patient})

@login_required
def diagnosis_detail(request,pk):
    diagnosis = get_object_or_404(Diagnosis, pk=pk)
    surveys = Survey.objects.filter(diagnosis=diagnosis)
    return render(request, 'diagnosis/diagnosis_detail.html', {'diagnosis': diagnosis,'surveys':surveys})

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
    #questions = Question.objects.all()
    context = {
        'form': form,
        'patients':patients,
        'questions':questions,
        'answers':answers,
        'inquirer':inquirer,
    }
    return render(request, 'diagnosis/diagnosis_new.html', context)

@permission_required('diagnosis.add_diagnosis')
@login_required
def save_diagnosis(request,pk):
    #if request.method == 'POST':
    #atomic: добавление диагностики и затем добавление опроса
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
        model = joblib.load('diagnosis/models/dermatology_model.pkl')
        predicate(answer_values,model)
    #считать из БД результаты опроса и отправить в функцию-обработчик (нейронная сеть)
    #добавить модель диагнозов. В зависимости от ответа НС выбирать Диагноз и выводить его пользователю. 
    #подготовить шаблон заключения
    return HttpResponseRedirect(reverse('main'))

@login_required
@permission_required('diagnosis.add_diagnosis')
def select_inquirer(request):
    user = request.user
    doctor = get_object_or_404(Doctor,login = user)
    specialty = doctor.specialty_id
    speciality_inquirers = SpecialityInquirer.objects.filter(specialty=specialty)
    return render(request, 'diagnosis/select_inquirer.html', {'inquirers': speciality_inquirers})