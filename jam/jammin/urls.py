from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('query', views.search, name="search"),
	path('<slug:username>_profile/query_<slug:query>', views.search_results, name='search_results'),
	path('query_<slug:query>', views.search_results, name='search_results'),
	path('signup/', views.user_signup, name='user_signup'),
	path('login/', views.user_login, name='user_login'),
	path('logout/', views.account_logout, name='logout'),
	path('employee_app/', views.employee_app, name='employee_application'),
	path('app_confirm/', views.app_confirm, name='application_confirmation'),
	path('employee_login/', views.employee_login, name='employee_login'),
	path('<slug:username>_profile/', views.user_profile, name="user_profile"),
	path('<slug:username>_profile/store/', views.user_store, name="user_store"),
	path('cart/', views.user_cart, name='cart'),
	path('<slug:username>_profile/store/add', views.add_item, name="add_item"),
	path('<slug:username>_profile/store/drop_<int:itemid>', views.drop_item, name="drop_item"),
	path('<slug:username>_profile/store/modify_<int:itemid>', views.modify_item, name="modify_item")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
