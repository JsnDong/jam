from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout

from . import models, forms

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

def user_cart(request):
	if request.user.is_authenticated:
		user = request.user.useraccount.userid
		items = models.CartHas.objects.filter(user_id = request.user.useraccount.userid)
		cart = list()
		for i in items:
			item = models.Item.objects.get(itemid = i.item_id)
			price = models.Sells.objects.get(item=i.item, seller_id=i.seller_id).price
			total = float(price) * float(i.quantity)
			cart = [i, item, total]
			cart += [cart]
		cart_total = models.Cart.objects.get(id = items[0].cart_id).total

		return render(request, "cart.html", {'account': request.user, 'cart':cart, 'total' : total})

def add_to_cart(request, itemid, author):
	if request.user.is_authenticated:
		user = request.user.useraccount.userid
		item = itemid
		seller = author
		quantity = 1
		#ITEM ALREADY IN CART JUST CHANGING QUANTITY
		try:
			carthas = models.CartHas.objects.get(user_id = user, item_id = item, seller_id = seller)
			carthas.quantity = carthas.quantity + quantity
			carthas.save()
			cartid = carthas.cart.id
			cart = models.Cart.objects.get(id = cartid)
		except (Exception):
			#ITEM NOT IN CART BUT CART EXISTS FOR THIS USER
			try:
				cart = models.CartHas.objects.get(user_id = user).id
			#ITEM NOT IN CART AND NO CART EXISTS FOR THE USER
			except (Exception):
				cart = models.Cart.objects.create_cart().id
			carthas = models.CartHas.objects.create_carthas(user, item, seller, cart, quantity)
		cart = models.Cart.objects.get(id = cart)
		price = models.Sells.objects.get(seller_id = seller, item_id = item).price
		cart.total = cart.total + quantity * float(price)
		cart.save()
	return render(request, 'search_results.html', {'account': request.user})
