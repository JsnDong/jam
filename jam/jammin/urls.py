from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.user_signup, name='user_signup'),
	path('login/', views.user_login, name='user_login'),
	path('logout/', views.account_logout, name='logout'),
	path('employee_app/', views.employee_app, name='employee_application'),
	path('app_confirm/', views.app_confirm, name='application_confirmation'),
	path('employee_login/', views.employee_login, name='employee_login'),
	path('<slug:username>_profile/', views.user_profile, name="user_profile"),
	path('<slug:username>_profile/store/', views.user_store, name="user_store"),
	path('<slug:username>_profile/store/add', views.add_item, name="Add Item to Store"),
	path('cart/', views.cart, name='cart'),
]
