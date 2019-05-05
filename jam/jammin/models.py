from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

from .managers import AccountManager, EmployeeManager

class Item(models.Model):
	itemid = models.AutoField(primary_key=True,\
							  validators=[MinValueValidator(100000000),
										  MaxValueValidator(999999999)])
	name = models.CharField(max_length=255, blank=False)

	def __str__(self):
		return self.name

class CartHas(models.Model):
	user = models.ForeignKey('UserAccount', models.CASCADE,
								null=False)
	item = models.ForeignKey('Item', models.CASCADE, blank=True,
								null=True)
	cart = models.ForeignKey('Cart', models.CASCADE, blank=True, null=False)
	quantity = models.IntegerField(blank=True, null=True,
								   validators=[MinValueValidator(0)])
	def __str__(self):
		return ", ".join([str(detail) for detail in [user, item, quantity]])
class Cart(models.Model):
	cart_has = models.ManyToManyField(Item, through='CartHas')
	total = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)])
	def __str__(self):
		return str(self.cart_has)+self.total

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
	account = models.OneToOneField(Account,
								   on_delete=models.CASCADE
	)

	userid = models.AutoField(primary_key=True,\
							  validators=[MinValueValidator(100000000),
										 	  MaxValueValidator(999999999)])
	username = models.CharField(max_length=255, unique=True)

	store = models.ManyToManyField(Item, through='Sells')
	cart = models.ManyToManyField(Cart, through='CartHas')
	#objects = UserManager()

	def __str__(self):
		return str(self.userid)

class Sells(models.Model):
	seller = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=11, decimal_places=2, null=True)
	quantity = models.IntegerField(validators=[MinValueValidator(1)])

	def __str__(self):
		return ", ".join([str(detail) for detail in [seller, item, price, quantity]])

class EmployeeAccount(models.Model):
	account = models.OneToOneField(
		Account,
		on_delete = models.CASCADE
	)

	employeeid = models.AutoField(primary_key=True,\
							      validators=[MinValueValidator(100000000),
										 	  MaxValueValidator(999999999)])
	salary = models.DecimalField(max_digits=11, decimal_places=2, null=True)
	wage = models.DecimalField(max_digits=11, decimal_places=2, null=True)

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
		return self.email
