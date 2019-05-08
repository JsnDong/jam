from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
#from django_countries.fields import CountryField
from .managers import AccountManager, EmployeeManager
from .choices import DEPT_CHOICES, DELIVERY_STATUS_CHOICES

from .validators import regex_validators

from PIL import Image
from io import BytesIO
import sys, os

#EMPLOYEES ARE ONLY USERS WHO CAN CHANGE THIS TABLE
class Shipping(models.Model):
	shipid = models.IntegerField(primary_key=True,\
							  validators=[MinValueValidator(0),
										  MaxValueValidator(999999999)])
	type = models.CharField(unique=True, max_length=255, null=False)
	price = models.IntegerField(validators=[MinValueValidator(0)], null=False)
	delivery_est = models.IntegerField(validators=[MinValueValidator(1)], null=False)

class Item(models.Model):
	itemid = models.AutoField(primary_key=True,\
							  validators=[MinValueValidator(100000000),
										  MaxValueValidator(999999999)])
	author = models.ForeignKey('UserAccount', on_delete=models.CASCADE, null=True)
	image = models.ImageField(upload_to='item_images', default='item_images/default.png', blank=True, null=True)
	thumbnail = models.ImageField(upload_to='thumbnails', blank=True, null=True)
	name = models.CharField(max_length=255, blank=False)
	dept = models.CharField(max_length=255, choices=DEPT_CHOICES, blank=False, default=None)
	description = models.TextField(blank=True, null=True)

	buys = models.PositiveIntegerField(default=0)
	views = models.PositiveIntegerField(default=0) 

	def __str__(self):
		return self.name
	def save(self):
		thumbnail_copy = ContentFile(self.image.read())
		thumbnail_output = BytesIO()
		thumbnail_pil = Image.open(thumbnail_copy)
		thumbnail_pil.thumbnail((100, 100))
		thumbnail_pil.save(thumbnail_output, format='PNG', quality=100)
		thumbnail_output.seek(0)
		thumbnail_name = os.path.basename(self.image.name).split('.')[0] + '_thumbnail.png'
		self.thumbnail = InMemoryUploadedFile(thumbnail_output, 'ImageField',\
											  thumbnail_name, 'image/png',\
											  sys.getsizeof(thumbnail_output), None)

		image_output = BytesIO()
		image_pil = Image.open(self.image)
		image_pil.thumbnail((500, 500))
		image_pil.save(image_output, format='PNG', quality=100)
		image_output.seek(0)
		image_name = os.path.basename(self.image.name).split('.')[0] + '.png'
		self.image = InMemoryUploadedFile(image_output, 'ImageField',\
											image_name, 'image/png',\
											sys.getsizeof(image_output), None)

		super(Item, self).save()


class Sells(models.Model):
	seller = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
	item = models.ForeignKey('Item', on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=11, decimal_places=2, null=True)
	quantity = models.IntegerField(validators=[MinValueValidator(1)])

	# def __str__(self):
	# 	return ", ".join([str(detail) for detail in [seller, item, price, quantity]])


class CartHas(models.Model):
	user = models.ForeignKey('UserAccount', models.CASCADE,
								null=False)
	item = models.ForeignKey('Item', models.CASCADE, blank=True,
								null=True)
	seller = models.ForeignKey('Sells', models.CASCADE, blank=True, null=True)
	cart = models.ForeignKey('Cart', models.CASCADE, blank=True, null=False)
	quantity = models.IntegerField(blank=True, null=False,
								   validators=[MinValueValidator(0)], default=1)
	#objects = CartHasManager()


	# def __str__(self):
	# 	return ", ".join([str(detail) for detail in [user, item, seller,  quantity]])


class Cart(models.Model):
	cart_has = models.ManyToManyField(Sells, through='CartHas')
	total = models.FloatField(blank=True, null=True, validators=[MinValueValidator(0)])
	ordered = models.BooleanField(default=False, null=False)
	def __str__(self):
		return str(self.cart_has)+str(self.total)


class Delivery(models.Model):
	tracking_code = models.CharField(max_length=6, blank=False)
	status = models.CharField(max_length=255, blank=False, choices=DELIVERY_STATUS_CHOICES, default='processing')
	carrier = models.CharField(max_length=255, blank=False)
	arrival_date = models.DateField(null=True)

class Order(models.Model):
	orderid = models.AutoField(primary_key=True,\
							  validators=[MinValueValidator(100000000),
										  MaxValueValidator(999999999)])
	cart = models.ForeignKey('Cart', models.CASCADE, null=False)
	date_placed = models.DateField(auto_now_add=True, null=False)
	card = models.ForeignKey('Card', models.CASCADE, null=True)
	address = models.ForeignKey('Address', models.CASCADE, null=False)
	shipping = models.ForeignKey('Shipping', models.CASCADE, null=True)
	complete = models.BooleanField(default='False', null=False)
	delivery = models.ForeignKey('Delivery', models.CASCADE, null=True)


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
	account = models.OneToOneField('Account',
								   on_delete=models.CASCADE
	)

	userid = models.AutoField(primary_key=True,\
							  validators=[MinValueValidator(100000000),
										  MaxValueValidator(999999999)])
	username = models.CharField(max_length=255, unique=True)
	store = models.ManyToManyField(Item, through='Sells')
	cart = models.ManyToManyField(Cart, through='CartHas')

	def __str__(self):
		return str(self.userid)

class EmployeeAccount(models.Model):
	account = models.OneToOneField(
		'Account',
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

class Card(models.Model):
	card_number = models.CharField(max_length=20, unique=True, blank=False, validators=[regex_validators])
	expiry_date = models.DateField(blank =False, null=True)
	cvn = models.CharField(max_length=200, blank= False)

	cardholder = models.CharField(max_length=200, unique=True, blank =False, null=True)
	user_account = models.ForeignKey('UserAccount', on_delete=models.CASCADE, related_name ="useracc_id")
	useraccounts = models.ManyToManyField(UserAccount)
	
	class Meta:
		unique_together = (('user_account','cardholder'),)

class Address(models.Model):
	street = models.CharField(max_length=255, blank=False)
	zipcode = models.CharField(max_length=5, blank=False)
	stateprovince =  models.CharField(max_length=255, blank=False)
	city = models.CharField(max_length=255, blank=False)
	country =  models.CharField(max_length=255, blank=False)
	name =  models.CharField(max_length=255, blank=False)

	currentAccount = models.ForeignKey('UserAccount', on_delete=models.CASCADE, related_name ="currUser_id")
	currentUser = models.ManyToManyField(UserAccount)
	
