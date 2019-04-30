from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import AccountManager

class Account(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255, blank=False)
	surname = models.CharField(max_length=255, blank=False)
	dob = models.DateField(null=True)

	joined = models.DateField(auto_now_add=True)
	seen = models.DateField(auto_now=True)
	is_active = models.BooleanField(default=True)

	is_admin = models.BooleanField(default=False)
	is_employee = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'surname']

	objects = AccountManager()

	def __str__(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin