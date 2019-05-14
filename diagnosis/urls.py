from django.urls import path, include
from . import views

urlpatterns = [
   # path('login/',views.login,name='login'),
    path('', views.main, name='main'),
    path('patients',views.patients_list,name='patients'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('diagnosis/<int:pk>/', views.diagnosis_detail, name='diagnosis_detail'),
    path('diagnosis/new/<int:pk>', views.diagnosis_new, name='diagnosis_new'),
    path('diagnosis/new/<int:pk>/save', views.save_diagnosis, name='save_diagnosis'),
    path('diagnosis/select_inquirer',views.select_inquirer,name='select_inquirer'),
    path('diagnosis/download/<int:pk>/',views.download_diagnosis_result,name='download_diagnosis_result'),
]