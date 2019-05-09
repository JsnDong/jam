from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout

from . import models, forms

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

'''
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

def add_to_cart(request, username, itemid):
	return render(request, 'cart.html')
'''

def index(request):
	all_items = models.Item.objects.all()

	most_viewed = list(all_items.order_by('-views'))[:10]

	return render(request, 'index.html', {'most_viewed': most_viewed})

def search(request):
	if request.method == 'POST' and\
	   request.POST['query']:
		query = request.POST['query']
		query = query.replace(" ", "_")
		return HttpResponseRedirect('/query_' + query)
	else:
		raise Http404

def search_results(request, query):
	user = request.user.useraccount
	query = query.replace("_", " ")
	query_set = models.Item.objects.filter(Q(name__icontains = query) |\
										   Q(dept__icontains = query) |\
										   Q(description__icontains = query))
	results = list(query_set)
	listings = list()
	for result in results:
		all_listings = result.sells_set.all()
		buyable = all_listings.exclude(seller=user)
		price = buyable.order_by("-price")
		best_price = price[0] if len(price) != 0 else None 
		listings += [[result, best_price]]
	results = listings
	return render(request, 'search_results.html', {'query' : query, 'results': results})

def user_profile(request, username):
	try:
		user = models.UserAccount.objects.get(username=username)
	except:
		raise Http404

	return render(request, "user_profile.html", {'user': user})


def user_store(request, username):
	try:
		user = models.UserAccount.objects.get(username=username)
	except:
		raise Http404

	return render(request, "user_store.html", {'user': user})

def view_item(request, item_id):
	user = request.user.useraccount
	item = models.Item.objects.get(pk=item_id)

	if item == None:
		raise Http404

	item.views += 1
	item.save()

	try:
		listing = models.Sells.objects.get(seller=user, item=item)
	except:
		listing = None


	listings = models.Sells.objects.filter(item=item).exclude(seller=user)
	best_price = listings.order_by("-price")[0] if len(list(listings)) > 0 else None

	return render(request, 'view_item.html', {'item': item, 'listing': listing, 'listings': listings, 'best_price': best_price})

def add_item(request):
	user = request.user.useraccount
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	if request.method == 'POST':
		item_form = forms.AddItemForm(request.POST, request.FILES)
		sells_form = forms.SellsForm(request.POST)

		if item_form.is_valid() and sells_form.is_valid():
			item = item_form.save(commit=False)
			item.author = user
			item.save()
			sells = sells_form.save(commit=False)
			sells.seller = user
			sells.item = item
			sells.save()

			if request.POST.get("another"):
				return HttpResponseRedirect(reverse('add_item'))

			elif request.POST.get("view"):
				return HttpResponseRedirect(reverse('view_item', kwargs={'item_id': item.itemid}))

	else:
		item_form = forms.AddItemForm()
		sells_form = forms.SellsForm()

	return render(request, "add_item.html", {'item_form': item_form, 'sells_form': sells_form})

def modify_item(request, item_id):
	user = request.user.useraccount
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	item = models.Item.objects.get(author=user.userid, itemid=item_id)
	if request.method == 'POST':
		item_form = forms.AddItemForm(request.POST, request.FILES, instance=item)
		if item_form.is_valid():
			item = item_form.save(commit=False)
			if not item.image:
				item.image = 'item_images/default.png'
			item.save() 
			return HttpResponseRedirect(reverse('view_item', kwargs={'item_id': item.itemid}))
	else:
		item_form = forms.AddItemForm(instance=item)

	return render(request, "modify_item.html", {'item_form': item_form})

def add_listing(request, item_id):
	user = request.user.useraccount
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	try:
		item = models.Item.objects.get(pk=item_id)
	except:
		raise Http404

	if request.method == 'POST':
		sells_form = forms.SellsForm(request.POST)
		if sells_form.is_valid:
			listing = sells_form.save(commit=False)
			listing.seller = user
			listing.item = item
			listing.save()
			return HttpResponseRedirect(reverse("view_item", kwargs={'item_id': item_id}))
	else:
		sells_form = forms.SellsForm()

	return render(request, 'add_listing.html', {'item': item, 'sells_form': sells_form})

def modify_listing(request, listing_id):
	user = request.user.useraccount
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	try:
		listing = models.Sells.objects.get(pk=listing_id, seller=user)
	except:
		raise Http404

	if request.method == 'POST':
		sells_form = forms.SellsForm(request.POST, instance=listing)
		if sells_form.is_valid():
			sells_form.save()
			return HttpResponseRedirect(reverse("view_item", kwargs={'item_id': listing.item.itemid}))
	else:
		sells_form = forms.SellsForm(instance=listing)

	return render(request, 'add_listing.html', {'item': listing.item, 'listing': listing, 'sells_form': sells_form})

def drop_listing(request, listing_id):
	user = request.user.useraccount
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	try:
		listing = models.Sells.objects.get(pk=listing_id, seller=user)
	except:
		raise Http404

	listing.delete()

	return HttpResponseRedirect(reverse("view_item", kwargs={'item_id': listing.item.itemid}))

def view_cart(request):
	return HttpResponseRedirect('/profile_'+request.user.useraccount.username)