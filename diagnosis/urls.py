from django.urls import path, include
from . import views

urlpatterns = [
   # path('login/',views.login,name='login'),
    path('', views.main, name='main'),
    path('patients',views.patients_list,name='patients'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('diagnosis/<int:pk>/', views.diagnosis_detail, name='diagnosis_detail'),
    path('diagnosis/new', views.diagnosis_new, name='diagnosis_new'),
    path('diagnosis/new/save', views.save_diagnosis, name='save_diagnosis'),

]