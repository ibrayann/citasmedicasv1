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
  path('citas_medicas/', views.citas_medicas, name='citas_medicas'),
  path('anular_cita/<int:id_cita>/', views.anular_cita, name='anular_cita'),
  path('agendarhora/', views.agendarhora, name='agendarhora'),

]