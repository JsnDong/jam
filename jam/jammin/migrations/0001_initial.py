# Generated by Django 2.2 on 2019-04-30 22:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('dob', models.DateField(null=True)),
                ('joined', models.DateField(auto_now_add=True)),
                ('seen', models.DateField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmployeeApp',
            fields=[
                ('candidateid', models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)])),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('dob', models.DateField(null=True)),
                ('resume', models.FileField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAccount',
            fields=[
                ('employeeid', models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)])),
                ('salary', models.DecimalField(decimal_places=2, max_digits=11, null=True)),
                ('wage', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subordinates', models.ManyToManyField(related_name='_employeeaccount_subordinates_+', to='jammin.EmployeeAccount')),
                ('supervisors', models.ManyToManyField(related_name='_employeeaccount_supervisors_+', to='jammin.EmployeeAccount')),
            ],
        ),
    ]
