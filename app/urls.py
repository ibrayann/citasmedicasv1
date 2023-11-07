from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('login/', views.login, name='login'),
  path('register/', views.register, name='register'),
  path('pacientes/', views.pacientes, name='pacientes'),
  path('logout', views.logout, name='logout'),
  path('medicos/', views.medicos, name='medicos'),
  path('agendamedica/<str:run>/', views.agendamedica, name='agendamedica'),
  path('agregardia/<str:run>/', views.agregardia, name='agregardia'),
  path('cambioDisponibilidad', views.cambioDisponibilidad, name='cambioDisponibilidad'),
  path('registermedico/', views.registermedico, name='registermedico'),

]