from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Account

class AccountCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
	
	class Meta:
		model = Account
		fields = ('email', 'name', 'surname', 'dob')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords Do Not Match")
		return password2

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class AccountChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Account
		fields = ('email', 'password', 'name', 'surname', 'dob', 'is_active', 'is_admin', 'is_employee')

	def clean_password(self):
		return self.initial['password']

class EmployeeAppForm(forms.Form):
	name = forms.CharField(label='First Name')
	surname = forms.CharField(label='Last Name')
	email = forms.EmailField(label='Email')
	#resume = forms.FileField(label="Resume")

class EmployeeLoginForm(forms.Form):
	employee_id = forms.CharField(label='Employee ID')
	password = forms.CharField(widget=forms.PasswordInput())