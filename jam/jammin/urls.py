from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('query', views.search, name="search"),
	path('query_<slug:query>', views.search_results, name='search_results'),
	path('item_<int:itemid>/', views.view_item, name='view_item'),
	path('item_<int:itemid>/add_listing', views.add_listing, name='view_item'),
	path('signup/', views.user_signup, name='user_signup'),
	path('login/', views.user_login, name='user_login'),
	path('logout/', views.account_logout, name='logout'),
	path('employee_app/', views.employee_app, name='employee_application'),
	path('app_confirm/', views.app_confirm, name='application_confirmation'),
	path('employee_login/', views.employee_login, name='employee_login'),
	path('<slug:username>_profile/', views.user_profile, name="user_profile"),
	path('<slug:username>_profile/store/', views.user_store, name="user_store"),
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
	path('<slug:username>_profile/store/add', views.add_item, name="add_item"),
	path('<slug:username>_profile/store/drop_<int:itemid>', views.drop_item, name="drop_item"),
	path('<slug:username>_profile/store/modify_<int:itemid>', views.modify_item, name="modify_item"),
	path('<slug:username>_profile/payment/', views.addview_card, name="view/add_card"),
	path('<slug:username>_profile/address/', views.addview_address, name="view/add_address"),
	path('<slug:username>_profile/payment/drop_<int:id>', views.drop_card, name="drop_card"),
	path('<slug:username>_profile/address/drop_<int:id>', views.drop_addr, name="drop_addr"),
	path('<slug:username>_profile/orders', views.user_orders, name="orders")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
