from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator

from .managers import AccountManager, EmployeeManager

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

class UserAccount(models.Model):
    alpha = RegexValidator(r'^[a-zA-Z]*$', 'Only letter characters are allowed.')
    first_name = models.CharField(max_length=200,blank =False,null=True,validators=[alpha])
    surname = models.CharField(max_length=200,blank =False,null=True,validators=[alpha])
    username = models.CharField(max_length=200, primary_key=True, unique=True,blank =False,null=True)
    userId = models.CharField(max_length=200, primary_key=True, unique=True)
    date_of_birth = models.DateField(blank =False,null=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)

class EmployeeAccount(models.Model):
	account = models.OneToOneField(
		Account,
		on_delete = models.CASCADE
	)

	employeeid = models.AutoField(primary_key=True,\
							      validators=[MinValueValidator(100000000),
										 	  MaxValueValidator(999999999)])
	salary = models.DecimalField(max_digits=11, decimal_places=2, null=True)
	wage = models.DecimalField(max_digits=4, decimal_places=2, null=True)

	subordinates = models.ManyToManyField('self')
	supervisors = models.ManyToManyField('self')

	objects = EmployeeManager()

	def __str__(self):
		return str(self.employeeid)

class EmployeeApp(models.Model):
	candidateid = models.AutoField(primary_key=True,\
								   validators=[MinValueValidator(100000000),
											   MaxValueValidator(999999999)])
	name = models.CharField(max_length=255, blank=False)
	surname = models.CharField(max_length=255, blank=False)
	email = models.EmailField(max_length=255, blank=False)
	dob = models.DateField(null=True)
	resume = models.FileField(blank=False)

	def __str__(self):
		return str.email

