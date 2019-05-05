from django.shortcuts import render
from django.urls import reverse
from django.http import	HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .forms import AddItemForm, AccountCreationForm, UserSignUpForm, LoginForm, SellsForm, EmployeeAppForm, EmployeeLoginForm
from . import models

def index(request):
	return render(request, 'index.html', {'account': request.user})

def search(request):
	if request.method == 'POST':
		query = request.POST.get('query')
		return HttpResponseRedirect('/query_' + query)
	else:
		return HttpResponseRedirect('/')

#def search_results(request, query):

def user_signup(request):
	if request.method == 'POST':
		account_form = AccountCreationForm(request.POST)
		user_form = UserSignUpForm(request.POST)
		if account_form.is_valid() and user_form.is_valid():
			account = account_form.save()
			user = user_form.save(commit=False)
			user.account = account
			user.save()
			return HttpResponseRedirect('/')
	else:
		account_form = AccountCreationForm()
		user_form = UserSignUpForm()

	return render(request, 'user_signup.html', {'account_form': account_form, 'user_form': user_form})

def user_login(request):
	if request.method == 'POST':
		login_form = LoginForm(request.POST)
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
		login_form = LoginForm()

	return render(request, 'login.html', {'login_form': login_form})

def account_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def employee_app(request):
	if request.method == 'POST':
		form = EmployeeAppForm(request.POST, request.FILES)
		if form.is_valid():
			candidate = form.save(commit=False)
			candidate.save()
			return HttpResponseRedirect('/app_confirm')
	else:
		form = EmployeeAppForm()

	return render(request, 'employee_app.html', {'form': form})

def app_confirm(request):
	return render(request, 'app_confirm.html')

def employee_login(request):
	if request.method == 'POST':
		form = EmployeeLoginForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/')
	else:
		form = EmployeeLoginForm()

	return render(request, 'employee_login.html', {'form': form})

def user_profile(request, username):
	if not request.user.is_authenticated or\
		   request.user.useraccount.username != username:
		return HttpResponseRedirect('/')

	return render(request, "user_profile.html", {'account': request.user})

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
		item_form = AddItemForm(request.POST, request.FILES)
		sells_form = SellsForm(request.POST)
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
		item_form = AddItemForm()
		sells_form = SellsForm()

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
		item_form = AddItemForm(request.POST, request.FILES, instance=item)
		sells_form = SellsForm(request.POST, instance=sells)
		if item_form.is_valid() and sells_form.is_valid():
			if not request.POST.get("cancel"):
				item = item_form.save(commit=False)
				item.author = request.user.useraccount
				item.save()
				sells = sells_form.save(commit=False)
				sells.seller = user
				sells.item = item
				sells.save()
			if request.POST.get("save"):
				return HttpResponseRedirect(reverse('user_store', kwargs={'username': user.username}))
		else:
			item_form = AddItemForm(instance=item)
			sells_form = SellsForm(instance=sells)

		return render(request, "modify_item.html", {'user': user,'item_form': item_form, 'sells_form': sells_form})

def user_cart(request, username):
	# if not request.user.is_authenticated or\
	# 	   request.user.useraccount.username != username:
	# 	return HttpResponseRedirect('/')
	#
	# user = request.user.useraccount
	# cart = user.cart.all()
	# listings = list()
	# for item in cart:
	# 	sells = models.Sells.objects.get(item=item.itemid, seller=user.userid)
	# 	listing = [item, sells]
	# 	listings += [listing]
	#
	# return render(request, "user_store.html", {'account': request.user, 'listings':listings})

	return render(request, 'cart.html')
