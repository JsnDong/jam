from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

from .managers import AccountManager, EmployeeManager
from .choices import DEPT_CHOICES

from PIL import Image
from io import BytesIO
import sys, os

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

	def __str__(self):
		return self.name

	def save(self):
		output = BytesIO()
		pil = Image.open(self.image)

		pil.thumbnail((500, 500))
		pil.save(output, format='PNG', quality=100)
		output.seek(0)
		image_name = os.path.basename(self.image.name).split('.')[0] + '.png'
		self.image = InMemoryUploadedFile(output, 'ImageField',\
									    image_name, 'image/png',\
									    sys.getsizeof(output), None)

		pil.thumbnail((100, 100))
		pil.save(output, format='PNG', quality=100)
		output.seek(0)
		image_name = os.path.basename(self.image.name).split('.')[0] + '_thumbnail.png'
		self.thumbnail = InMemoryUploadedFile(output, 'ImageField',\
									    image_name, 'image/png',\
									    sys.getsizeof(output), None)
		super(Item, self).save()

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

	store = models.ManyToManyField('Item', through='Sells')

	def __str__(self):
		return str(self.userid)

class Sells(models.Model):
	seller = models.ForeignKey('UserAccount', on_delete=models.CASCADE)
	item = models.ForeignKey('Item', on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=11, decimal_places=2, null=True)
	quantity = models.IntegerField(validators=[MinValueValidator(1)])

	def __str__(self):
		return ", ".join([str(detail) for detail in [seller, item, price, quantity]])

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
	card_number = models.CharField(max_length=16, unique=True, blank=False)
	expiry_date = models.DateField(blank =False, null=True)
	cvn = models.IntegerField(default = 000,blank=False,validators=[MinValueValidator(100),
										 	  MaxValueValidator(999)])
	cardholder = models.CharField(max_length=200, unique=True, blank =False, null=True)
	user_account = models.ForeignKey('UserAccount', on_delete=models.CASCADE, related_name ="useracc_id")
	useraccounts = models.ManyToManyField(UserAccount)
	
	class Meta:
		unique_together = (('user_account','cardholder'),)