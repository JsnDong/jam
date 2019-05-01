from django.urls import path

from . import views

urlpatterns = [
	path('app_confirm/', views.app_confirm, name='application_confirmation'),
	path('employee_app/', views.employee_app, name='employee_application'),
	path('employee_login/', views.employee_login, name='employee_login'),
	path('', views.index, name='index'),
]