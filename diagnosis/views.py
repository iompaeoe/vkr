from django.shortcuts import render, get_object_or_404
from .models import Patient, Diagnosis, Question, Answer, Doctor, Survey
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import DiagnosisForm
from django.db import transaction
from django.conf import settings
from django.utils import timezone

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
def diagnosis_new(request):
    form = DiagnosisForm()
    patients = Patient.objects.all()
    questions = Question.objects.all()
    answers = Answer.objects.all()
    context = {
        'form': form,
        'patients':patients,
        'questions':questions,
        'answers':answers,
    }
    return render(request, 'diagnosis/diagnosis_new.html', context)

@permission_required('diagnosis.add_diagnosis')
@login_required
def save_diagnosis(request):
    #if request.method == 'POST':
    #atomic: добавление диагностики и затем добавление опроса
    with transaction.atomic():
        patient_code = request.POST.get('patient')
        patient = get_object_or_404(Patient,id=patient_code)
        doctor_code = request.POST.get('doctor')
        user = get_object_or_404(User,username=doctor_code)
        doctor = get_object_or_404(Doctor,login = user)
        diagnosis_date = timezone.now()
        diagnosis = Diagnosis(patient=patient,doctor=doctor,diagnosis_date=diagnosis_date)
        diagnosis.save()
        questions = Question.objects.all()
        for question in questions:
            answer_code = request.POST.get('answerRadioForQuestion{0}'.format(question.id))
            answer = get_object_or_404(Answer,id=answer_code)
            survey = Survey(diagnosis=diagnosis, question=question, answer=answer)
            survey.save()



    #считать из БД результаты опроса и отправить в функцию-обработчик (нейронная сеть)
    #добавить модель диагнозов. В зависимости от ответа НС выбирать Диагноз и выводить его пользователю. 
    #подготовить шаблон заключения
    return HttpResponseRedirect(reverse('main'))
