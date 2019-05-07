from django.db import models
from django.contrib.auth.base_user import BaseUserManager

class AccountManager(BaseUserManager):
	def create_user(self, email, name, surname, password):
		if not email:
			raise ValueError('An Email is Required')

		user = self.model(email = self.normalize_email(email),\
						  name = name,\
						  surname = surname)

		user.set_password(password)

		user.save()
		return user

	def create_superuser(self, email, name, surname, password):
		user = self.create_user(email,\
								name = name,\
								surname = surname,\
								password = password)

		user.is_superuser = True
		user.is_admin = True
		user.is_employee = True

		user.save()
		return user

class EmployeeManager(models.Manager):
	def create_employee(self, account, name, surname):
		employee = self.create(account = account)
		employee.save()
		return employee

class CartManager(models.Manager):
	def create_cart(self):
		cart = self.model(total = 0)
		cart.save()
		return cart
class CartHasManager(models.Manager):
	def create_carthas(self, user, item, seller, cart, quantity):
		carthas = self.model(1, item, seller, cart, quantity)
		carthas.save()
		return carthas


