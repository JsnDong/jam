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

'''
class UserManager(model.Managers):
	def create_user(self, username):
		user = self.create(username = username)
		user.save()
		return user
'''


class EmployeeManager(models.Manager):
	def create_employee(self, account, name, surname):
		employee = self.create(account = account)
		employee.save()
		return employee


