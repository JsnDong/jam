from django.shortcuts import render
from django.http import	HttpResponse, HttpResponseRedirect

from .forms import EmployeeAppForm, EmployeeLoginForm

def index(request):
	return render(request, 'index.html')

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