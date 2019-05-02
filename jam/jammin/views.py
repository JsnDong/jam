from django.shortcuts import render
from django.http import	HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from .forms import AccountCreationForm, UserSignUpForm, LoginForm, EmployeeAppForm, EmployeeLoginForm

def index(request):
	return render(request, 'index.html', {'account': request.user})

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
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	return render(request, "user_profile.html")

def user_store(request, username):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	return render(request, "user_store.html")

def add_item(request, username):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/')

	#if request.method='POST':
