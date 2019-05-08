from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout
from . import models, forms
from .forms import AddItemForm, AddAddress, AccountCreationForm, UserSignUpForm, LoginForm, SellsForm, EmployeeAppForm, EmployeeLoginForm, AddPaymentOption

def index(request):
	most_viewed = list(models.Item.objects.all().order_by('-views'))[:10]

	return render(request, 'index.html', {'account': request.user, 'most_viewed': most_viewed})

def search(request):
	if request.method == 'POST':
		query = request.POST.get('query')
		query = query.replace(" ", "_")
		return HttpResponseRedirect('/query_' + query, {'account' : request.user})
	else:
		return HttpResponseRedirect('/')

def search_results(request, query):
	query = query.replace("_", " ")
	query_set = models.Item.objects.filter(Q(name__icontains = query) |\
										   Q(dept__icontains = query) |\
										   Q(description__icontains = query))
	result = list(query_set)
	
	return render(request, 'search_results.html', {'account': request.user, 'result' : result, 'search' : query})

def view_item(request, itemid):
	item = models.Item.objects.get(itemid=itemid)

	if item == None:
		raise Http404

	item.views += 1
	item.save()

	listings = list(models.Sells.objects.filter(item=itemid))

	return render(request, 'view_item.html', {'account': request.user, 'item': item, 'listings': listings})

def add_listing(request, itemid):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	item = models.Item.objects.get(itemid=itemid)
	if item == None:
		raise Http404

	try:
		listing = models.Sells.objects.get(seller=request.user.useraccount, item=itemid)
	except:
		listing = None

	if listing and request.method == 'POST':
		sells_form = forms.SellsForm(request.POST, instance=listing)
		if sells_form.is_valid():
			sells_form.save()
			return HttpResponseRedirect(reverse("user_store", kwargs={'username': request.user.useraccount.username}))
	elif not listing and request.method == 'POST':
		sells_form = forms.SellsForm(request.POST)
		if sells_form.is_valid:
			listing = sells_form.save(commit=False)
			listing.seller = request.user.useraccount
			listing.item = item
			listing.save()
			return HttpResponseRedirect(reverse("user_store", kwargs={'username': request.user.useraccount.username}))
	elif listing:
		sells_form = forms.SellsForm(instance=listing)
	else:
		sells_form = forms.SellsForm(instance=listing)

	return render(request, 'add_listing.html', {'account': request.user, 'item': item, 'sells_form': sells_form})

def search(request):
	if request.method == 'POST':
		query = request.POST.get('query')
		query = query.replace(" ", "_")
		return HttpResponseRedirect('/query_' + query)
	else:
		return HttpResponseRedirect('/')

def search_results(request, query):
	if request.method == 'GET':
		query = query.replace("_", " ")
		query_set = models.Item.objects.filter(Q(name__icontains = query) | Q(dept__icontains = query) | Q(description__icontains = query))
		result = list()
		for item in query_set:
			temp = [item.name, item.description]
			result += [temp]
	return render(request, 'search_results.html', {'result' : result, 'search' : query, 'account': request.user})
def user_signup(request):
	if request.method == 'POST':
		account_form = forms.AccountCreationForm(request.POST)
		user_form = forms.UserSignUpForm(request.POST)
		if account_form.is_valid() and user_form.is_valid():
			account = account_form.save()
			user = user_form.save(commit=False)
			user.account = account
			user.save()
			return HttpResponseRedirect('/')
	else:
		account_form = forms.AccountCreationForm()
		user_form = forms.UserSignUpForm()

	return render(request, 'user_signup.html', {'account_form': account_form, 'user_form': user_form})

def user_login(request):
	if request.method == 'POST':
		login_form = forms.LoginForm(request.POST)
		if login_form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			account = authenticate(request, email=email, password=password)
			if account is not None:
				login(request, account)
				return HttpResponseRedirect('/')
			else:
				return HttpResponseRedirect('/login')
	else:
		login_form = forms.LoginForm()

	return render(request, 'login.html', {'login_form': login_form})

def account_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def employee_app(request):
	if request.method == 'POST':
		form = forms.EmployeeAppForm(request.POST, request.FILES)
		if form.is_valid():
			candidate = form.save(commit=False)
			candidate.save()
			return HttpResponseRedirect('/app_confirm')
	else:
		form = forms.EmployeeAppForm()

	return render(request, 'employee_app.html', {'form': form})

def app_confirm(request):
	return render(request, 'app_confirm.html')

def employee_login(request):
	if request.method == 'POST':
		form = forms.EmployeeLoginForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/')
	else:
		form = forms.EmployeeLoginForm()

	return render(request, 'employee_login.html', {'form': form})

def user_profile(request, username):
	profile = models.UserAccount.objects.get(username=username)

	return render(request, "user_profile.html", {'account': request.user, 'profile': profile})

def user_store(request, username):
	if not request.user.is_authenticated or\
		   request.user.useraccount.username != username:
		return HttpResponseRedirect('/')

	user = request.user.useraccount
	store = user.store.all()
	listings = list()
	for item in store:
		sells = models.Sells.objects.get(item=item.itemid, seller=user.userid)
		listing = [item, sells]
		listings += [listing]

	return render(request, "user_store.html", {'account': request.user, 'listings':listings})

def add_item(request, username):
	if request.method == 'POST':
		item_form = forms.AddItemForm(request.POST, request.FILES)
		sells_form = forms.SellsForm(request.POST)
		if item_form.is_valid() and sells_form.is_valid():
			user = request.user.useraccount
			if not request.POST.get("cancel"):
				item = item_form.save(commit=False)
				item.author = request.user.useraccount
				item.save()
				sells = sells_form.save(commit=False)
				sells.seller = user
				sells.item = item
				sells.save()
			if request.POST.get("another"):
				return HttpResponseRedirect(reverse('add_item', kwargs={'username': user.username}))
			else:
				return HttpResponseRedirect(reverse('user_store', kwargs={'username': user.username}))
	else:
		item_form = forms.AddItemForm()
		sells_form = forms.SellsForm()

	return render(request, "add_item.html", {'item_form': item_form, 'sells_form': sells_form})

def drop_item(request, username, itemid):
	if not request.user.is_authenticated or\
		   request.user.useraccount.username != username:
		return HttpResponseRedirect('/')

	user = request.user.useraccount
	sells= models.Sells.objects.get(seller=user.userid, item=itemid)
	sells.delete()
	models.Item.objects.filter(itemid=itemid, useraccount=None).delete()

	return HttpResponseRedirect(reverse('user_store', kwargs={'username': user.username}))

def modify_item(request, username, itemid):
	if not request.user.is_authenticated or\
		   request.user.useraccount.username != username:
		return HttpResponseRedirect('/')

	user = request.user.useraccount
	item = models.Item.objects.get(author=user.userid, itemid=itemid)
	sells = models.Sells.objects.get(seller=user.userid, item=itemid)
	if request.method == 'POST':
		item_form = forms.AddItemForm(request.POST, request.FILES, instance=item)
		sells_form = forms.SellsForm(request.POST, instance=sells)
		if item_form.is_valid() and sells_form.is_valid():
			item_form.save()
			sells_form.save()
			return HttpResponseRedirect(reverse('user_store', kwargs={'username': user.username}))
	else:
		item_form = forms.AddItemForm(instance=item)
		sells_form = forms.SellsForm(instance=sells)

	return render(request, "modify_item.html", {'account': request.user,'item_form': item_form, 'sells_form': sells_form})

def take_item(elem):
	return elem[1].itemid

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
				price = models.Sells.objects.get(item=item, seller=i.seller.id).price
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
		seller = author
		quantity = 1
		#ITEM ALREADY IN CART JUST CHANGING QUANTITY
		try:
			t = inc_cart_item(request, itemid, author)
			return t
		except (Exception):
			#ITEM NOT IN CART BUT CART EXISTS FOR THIS USER
			try:
				cartboi = models.CartHas.objects.filter(user_id = user)
				cart_all = cartboi.filter(ordered=False)
				cart = cartboi[0].cart.id
			#ITEM NOT IN CART AND NO CART EXISTS FOR THE USER
			except (Exception):
				cart = models.Cart.objects.create(total=0).id
			carthas = models.CartHas.objects.create(quantity=quantity, user_id=user, item_id=item, seller_id=seller, cart_id=cart)
		cart = models.Cart.objects.get(id = cart)
		price = models.Sells.objects.get(seller_id = seller, item_id = item).price
		cart.total = cart.total + quantity * float(price)
		cart.save()
		cartid = carthas.cart.id
		return HttpResponseRedirect('/cart/')
	return HttpResponseRedirect('/')


def item_change_cart_quantity(request, itemid, author, quantity):
	if request.user.is_authenticated:
		user = request.user.useraccount
		cart_t = user.cart.filter(ordered=False)
		carthass = models.CartHas.objects.filter(cart=cart_t[0], item_id = itemid, seller_id = author)
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
		price = models.Sells.objects.get(seller_id = author, item_id = itemid).price
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
	order.cart.ordered = 'True'
	order.cart.save()
	total = float(order.cart.total) + float(order.shipping.price)
	return render(request, 'order_confirm.html', {'order' : order, 'total' : total})

# def order_confirm(request, orderid):
# 	#delivery stuffs
# 	return render('')

def cancel_checkout(request, orderid):
	order = models.Order.objects.get(orderid=orderid).delete()
	return user_cart(request)


def cancel_checkout_no_order(request):
	return user_cart(request)

#added view for adding and viewing current cards
def addview_card(request, username):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')
	
	uid = request.user.useraccount.userid
	cardQuerySet = models.Card.objects.filter(user_account_id=uid) #usersCards is a queryset
	yourCardsList = list(cardQuerySet)
	
	if request.method == 'POST':
		card_form = AddPaymentOption(request.POST, request.FILES)
		if card_form.is_valid():
			user = request.user.useraccount
			card = card_form.save(commit=False)
			card.user_account = request.user.useraccount
			card.save()
			return HttpResponseRedirect(reverse('view/add_card', kwargs={'username': request.user.useraccount.username}))

	else:
		card_form = AddPaymentOption()
	
	return render(request, "addview_card.html", {'card_form': card_form, 'yourCardsList': yourCardsList, 'myuser': request.user})
def drop_card(request, username, id):
	if not request.user.is_authenticated or\
		   request.user.useraccount.username != username:
		return HttpResponseRedirect('/')

	user = request.user.useraccount
	cardToDelete = models.Card.objects.get(pk=id,user_account=user)
	
	cardToDelete.delete()

	return HttpResponseRedirect(reverse('view/add_card', kwargs={'username': user.username}))

def addview_address(request, username):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')
	
	uid = request.user.useraccount.userid
	addrQuerySet = models.Address.objects.filter(currentAccount_id=uid) #usersCards is a queryset
	yourAddrList = list(addrQuerySet)
	
	if request.method == 'POST':
		addr_form = AddAddress(request.POST, request.FILES)
		if addr_form.is_valid():
			user = request.user.useraccount
			addr = addr_form.save(commit=False)
			addr.currentAccount = request.user.useraccount
			addr.save()
			return HttpResponseRedirect(reverse('view/add_address', kwargs={'username': request.user.useraccount.username}))

	else:
		addr_form = AddAddress()
	
	return render(request, "addview_address.html", {'addr_form': addr_form, 'yourAddrList': yourAddrList, 'myuser': request.user})

def drop_addr(request, username, id):
	if not request.user.is_authenticated or\
		   request.user.useraccount.username != username:
		return HttpResponseRedirect('/')

	user = request.user.useraccount
	addrToDelete = models.Address.objects.get(pk=id,currentAccount=user)

	addrToDelete.delete()

	return HttpResponseRedirect(reverse('view/add_address', kwargs={'username': user.username}))
