from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	path('signup/', views.user_signup, name='user_signup'),

	path('login/', views.user_login, name='user_login'),

	path('logout/', views.account_logout, name='logout'),

	path('employee_app/', views.employee_app, name='employee_application'),

	path('app_confirm/', views.app_confirm, name='application_confirmation'),

	path('employee_login/', views.employee_login, name='employee_login'),

	re_path(r'^$',\
			views.index,
			name='index'),

	re_path(r'^query$',\
			views.search,\
			name='search'),

	re_path(r'^query_(?P<query>[A-Za-z0-9_]+)?$',\
			views.search_results,\
			name='search_results'),

	re_path(r'^item_(?P<item_id>[0-9]+)/$',\
			views.view_item,\
			name='view_item'),

	re_path(r'^add_item$',\
			views.add_item,\
			name='add_item'),

	re_path(r'modify_item_(?P<item_id>[0-9]+)$',\
			views.modify_item,\
			name='modify_item'),

	re_path(r'add_listing_(?P<item_id>[0-9]+)$',\
			views.add_listing,\
			name='add_listing'),

	re_path(r'drop_listing_(?P<listing_id>[0-9]+)$',\
			views.drop_listing,\
			name='drop_listing'),

	re_path(r'modify_listing_(?P<listing_id>[0-9]+)$',\
			views.modify_listing,\
			name='modify_listing'),

	re_path(r'^profile_(?P<username>[A-Za-z0-9]+)/$',\
			views.user_profile,\
			name="user_profile"),

	re_path(r'^profile_(?P<username>[A-Za-z0-9]+)/store$',\
		    views.user_store,\
		    name='user_store'),

	re_path(r'^profile_(?P<username>[A-Za-z0-9]+)/payment/$',\
		    views.add_view_card,\
		    name='add_view_card'),

	re_path(r'^profile_(?P<username>[A-Za-z0-9]+)/address/$',\
		    views.add_view_address,\
		    name='add_view_address'),

	re_path(r'^profile_(?P<username>[A-Za-z0-9]+)/payment/drop_card_(?P<card_id>[0-9]+)$',\
			views.drop_card,\
			name="drop_card"),

	re_path(r'^profile_(?P<username>[A-Za-z0-9]+)/address/drop_address_(?P<address_id>[0-9]+)$',\
			views.drop_address,\
			name="drop_address"),

	path('cart/', views.user_cart, name='cart'),
	path('add_to_cart_<int:itemid>_<int:author>', views.add_to_cart, name="add_to_cart"),
	path('cart/inc_cart_item_<int:itemid>_<int:seller>', views.inc_cart_item, name="inc_cart_item"),
	path('cart/dec_cart_item_<int:itemid>_<int:seller>', views.dec_cart_item, name="dec_cart_item"),
	path('cart/delete_cart_item_<int:itemid>_<int:seller>', views.delete_cart_item, name='delete_cart_item'),
	path('checkout', views.checkout, name="checkout"),
	path('checkout_address_<int:id>', views.checkout_address, name="checkout_address"),
	path('checkout_shipping_<int:orderid>_<int:shipid>', views.checkout_shipping, name="checkout_shipping"),
	path('checkout_card_<int:orderid>_<int:id>', views.checkout_card, name="checkout_card"),
	path('cancel_checkout_<int:orderid>', views.cancel_checkout, name="cancel_checkout"),
	path('cancel_checkout_no_order', views.cancel_checkout_no_order, name="cancel_checkout_no_order"),
	path('profile_<slug:username>/orders', views.user_orders, name="orders")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
