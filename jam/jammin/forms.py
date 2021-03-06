from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Item, Sells, Account, UserAccount, EmployeeApp, Card, Address, Cart

class AddItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ('image', 'name', 'dept', 'description')

	def save(self, commit=True):
		item = super().save(commit=False)
		if commit:
			item.save()
		return item

	def clean_dept(self):
		dept = self.cleaned_data['dept']
		if dept == None:
			raise forms.ValidationError('Select a category')
		return dept
class PaymentForm(forms.ModelForm):
	class Meta:
		model = Card
		fields = ('card_number', 'expiry_date', 'cvn', 'cardholder')

	def save(self, commit=True):
		card = super().save(commit=False)
		if commit:
			card.save()
		return card

class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = ('name','street','zipcode','country', 'stateprovince', 'city')

	def save(self, commit=True):
		address = super().save(commit=False)
		if commit:
			address.save()
		return address

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

class UserSignUpForm(forms.ModelForm):
	class Meta:
		model = UserAccount
		fields = ('username',)

	def save(self, commit=True):
		user = super().save(commit=False)
		if commit:
			user.save()
		return user

class EmployeeAppForm(forms.ModelForm):
	class Meta:
		model = EmployeeApp
		fields = ('name', 'surname', 'email', 'dob', 'resume')

	def save(self, commit=True):
		app = super().save(commit=False)
		if commit:
			app.save()
		return app

class LoginForm(forms.Form):
	email = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())

class EmployeeLoginForm(forms.Form):
	employee_id = forms.CharField(label='Employee ID')
	password = forms.CharField(widget=forms.PasswordInput())

class SellsForm(forms.ModelForm):
	class Meta:
		model = Sells
		fields = ('price', 'quantity')

	def save(self, commit=True):
		sells = super().save(commit=False)
		if commit:
			sells.save()
		return sells