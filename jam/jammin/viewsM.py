from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from . import models, forms

def id_in_list(order, orders):
	for i in range (0, len(orders)):
		if(order.orderid == orders[i].orderid):
			return True
	return False

def user_orders(request, username):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')
	try:
		carts = request.user.useraccount.cart.filter(ordered='True')
		orders = list()
		total = list()
		for cart in carts:
			temp = models.Order.objects.filter(cart=cart, complete='True')
			if not id_in_list(temp[0], orders):
				orders += temp
	except (Exception):
		orders = list()
	return render(request, 'user_orders.html', {'orders' : orders, 'username': username})


def user_cart(request):
	if request.user.is_authenticated:
		user = request.user.useraccount
		cart_len = 0
		try:
			cart_t = user.cart.filter(ordered=False)
			carthas = models.CartHas.objects.filter(cart=cart_t[0])
			cart = list()
			for i in carthas:
				item = models.Item.objects.get(itemid=i.item.itemid)
				price = i.seller.price
				total = float(price) * float(i.quantity)
				cart_len = cart_len + i.quantity
				cartt = [i, item, total]
				cart += [cartt]
			cart_total = cart_t[0].total
		except (Exception):
			cart = list()
			cart_total = 0.00
		return render(request, "cart.html", {'account': request.user, 'cart':cart, 'total' : cart_total, 'cart_len' : cart_len})
	cart = list()
	cart_total = 0.00
	return render(request, "cart.html", {'account': request.user, 'cart':cart, 'total' : cart_total, 'cart_len' : len(cart)})

def add_to_cart(request, itemid, author):
	if request.user.is_authenticated:
		user = request.user.useraccount.userid
		item = itemid
		seller = models.Sells.objects.get(seller_id = author, item_id = item)
		quantity = 1
		#ITEM ALREADY IN CART JUST CHANGING QUANTITY
		try:
			t = inc_cart_item(request, itemid, seller.id)
			return t
		except (Exception):
			#ITEM NOT IN CART BUT CART EXISTS FOR THIS USER
			try:
				cart_t = request.user.useraccount.cart.filter(ordered=False)
				cartboi = models.CartHas.objects.filter(cart=cart_t[0])
				for boi in cartboi:
					cart = cartboi[0].cart.id
				x = cart
			#ITEM NOT IN CART AND NO CART EXISTS FOR THE USER
			except (Exception):
				cart = models.Cart.objects.create(total=0).id
			carthas = models.CartHas.objects.create(quantity=quantity, user_id=user, item_id=item, seller=seller, cart_id=cart)
		cart = models.Cart.objects.get(id = cart)
		price = models.Sells.objects.get(seller_id = author, item_id = item).price
		cart.total = cart.total + quantity * float(price)
		cart.save()
		cartid = carthas.cart.id
		return HttpResponseRedirect('/cart/')
	return HttpResponseRedirect('/')


def item_change_cart_quantity(request, itemid, seller, quantity):
	if request.user.is_authenticated:
		user = request.user.useraccount
		cart_t = user.cart.filter(ordered=False)
		# seller = models.Sells.objects.get(seller_id = author, item_id = itemid)
		carthass = models.CartHas.objects.filter(cart=cart_t[0], item_id = itemid, seller = seller)
		carthas = carthass[0]
		if quantity == 2:
			quantity = (-1)*carthas.quantity
			carthas.delete()
		else:
			carthas.quantity = carthas.quantity + quantity
			if carthas.quantity == 0:
				carthas.delete()
			else:
				carthas.save()
		cartid = carthas.cart.id
		cart = models.Cart.objects.get(id = cartid)
		price = models.Sells.objects.get(id=seller).price
		# price = models.Sells.objects.get(seller_id = seller.seller, item_id = itemid).price
		cart.total = cart.total + quantity * float(price)
		cart.save()
		return HttpResponseRedirect('/cart/')
	return HttpResponseRedirect('/')


def inc_cart_item(request, itemid, seller):
	return item_change_cart_quantity(request, itemid, seller, 1)
def dec_cart_item(request, itemid, seller):
	return item_change_cart_quantity(request, itemid, seller, -1)
def delete_cart_item(request, itemid, seller):
	return item_change_cart_quantity(request, itemid, seller, 2)

def checkout(request):
	try:
		address = models.Address.objects.filter(currentAccount_id=request.user.useraccount.userid)
		addresses = list(address)
	except (Exception):
		addresses = list()
	return render(request, 'checkout_address.html', {'addr': addresses})

def checkout_address(request, id):
	ship = models.Shipping.objects.all()
	cart = request.user.useraccount.cart.filter(ordered=False)
	cart = cart[0]
	address = models.Address.objects.get(id=id)
	order = models.Order.objects.create(cart=cart, address=address)
	return render(request, 'checkout_shipping.html', {'ship' : ship, 'order' : order})


def checkout_shipping(request, orderid, shipid):
	order = models.Order.objects.get(orderid=orderid)
	ship = models.Shipping.objects.get(shipid=shipid)
	order.shipping = ship
	order.save()
	try:
		cards_t = models.Card.objects.filter(user_account_id=request.user.useraccount.userid)
		cards = list(cards_t)
	except (Exception):
		cards = list()
	return render(request, 'checkout_card.html', {'order' : order, 'cards' : cards})

def checkout_card(request, orderid, id):
	order = models.Order.objects.get(orderid=orderid)
	card = models.Card.objects.get(id=id)
	order.card = card
	order.complete = 'True'
	order.delivery = models.Delivery.objects.create(tracking_code=str(orderid*100), carrier="FedEx")
	order.save()
	cart = order.cart
	carthas = models.CartHas.objects.filter(cart=cart)
	for item in carthas:
		x = item.item.itemid
		listing = item.seller
		listing.quantity = listing.quantity - item.quantity
		if float(listing.quantity) < 0:
			cancel_checkout(request, orderid)
			return render(request, 'order_confirm.html', {'order' : order, 'total' : 0})
		listing.save()
	order.cart.ordered = 'True'
	order.cart.save()
	total = float(order.cart.total) + float(order.shipping.price)
	return render(request, 'order_confirm.html', {'order' : order, 'total' : total})

def cancel_checkout(request, orderid):
	order = models.Order.objects.get(orderid=orderid).delete()
	return user_cart(request)


def cancel_checkout_no_order(request):
	return user_cart(request)
