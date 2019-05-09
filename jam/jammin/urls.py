from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	re_path(r'^$',\
			views.index,
			name='index'),

	re_path(r'^query?$',\
			views.search,\
			name="search"),

	re_path(r'^query_(?P<query>[A-Za-z0-9_]+)?$',\
			views.search_results,\
			name='search_results'),

	re_path(r'^item_(?P<item_id>[0-9]+)/$',\
			views.view_item,\
			name='view_item'),

	re_path(r'^add_item$',\
			views.add_item,\
			name="add_item"),

	re_path(r'modify_item_(?P<item_id>[0-9]+)$',\
			views.modify_item,\
			name="modify_item"),

	re_path(r'add_listing_(?P<item_id>[0-9]+)$',\
			views.add_listing,\
			name="add_listing"),

	re_path(r'drop_listing_(?P<listing_id>[0-9]+)$',\
			views.drop_listing,\
			name="drop_listing"),

	re_path(r'modify_listing_(?P<listing_id>[0-9]+)$',\
			views.modify_listing,\
			name="modify_listing"),

	re_path(r'^profile_(?P<username>[A-Za-z0-9]+)/$',\
			views.user_profile,\
			name="user_profile"),

	re_path(r'profile_(?P<username>[A-Za-z0-9]+)/store',\
		    views.user_store,\
		    name="user_store"),

	path('signup/', views.user_signup, name='user_signup'),

	path('login/', views.user_login, name='user_login'),

	path('logout/', views.account_logout, name='logout'),

	path('employee_app/', views.employee_app, name='employee_application'),

	path('app_confirm/', views.app_confirm, name='application_confirmation'),

	path('employee_login/', views.employee_login, name='employee_login'),
	
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
