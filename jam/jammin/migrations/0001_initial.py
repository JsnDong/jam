# Generated by Django 2.2 on 2019-05-13 16:37

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
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator("^[A-Za-z \\']+$")])),
                ('street', models.CharField(max_length=255)),
                ('stateprovince', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator("^[A-Za-z \\']+$")])),
                ('city', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator("^[A-Za-z \\']+$")])),
                ('country', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator("^[A-Za-z \\']+$")])),
                ('zipcode', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^[0-9]{5}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardholder', models.CharField(max_length=200, validators=[django.core.validators.RegexValidator("^[A-Za-z \\']+$")])),
                ('card_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('^[0-9]{16}$')])),
                ('expiry_date', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^(1[0-2])|(0?[1-9])/[0-9]{2}$')])),
                ('cvn', models.CharField(max_length=3, validators=[django.core.validators.RegexValidator('^[0-9]{3}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('ordered', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CartHas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('cart', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='jammin.Cart')),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_code', models.CharField(max_length=6)),
                ('status', models.CharField(choices=[(None, 'SELECT'), ('processing', 'PROCESSING'), ('transit', 'IN TRANSIT'), ('shipped', 'SHIPPED'), ('delivered', 'DELIVERED')], default='delivered', max_length=255)),
                ('carrier', models.CharField(max_length=255)),
                ('arrival_date', models.DateField(null=True)),
            ],
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
            name='Item',
            fields=[
                ('itemid', models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)])),
                ('image', models.ImageField(blank=True, default='item_images/default.png', null=True, upload_to='item_images')),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails')),
                ('name', models.CharField(max_length=255)),
                ('dept', models.CharField(choices=[(None, 'SELECT'), ('brass', 'BRASS'), ('strings', 'STRINGS'), ('woodwind', 'WOODWIND'), ('percussion', 'PERCUSSION'), ('keyboard', 'KEYBOARD'), ('other', 'OTHER')], default=None, max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('buys', models.PositiveIntegerField(default=0)),
                ('views', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Sells',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11, null=True)),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jammin.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('shipid', models.IntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(999999999)])),
                ('type', models.CharField(max_length=255, unique=True)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('delivery_est', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('userid', models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)])),
                ('username', models.CharField(max_length=255, unique=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('addresses', models.ManyToManyField(to='jammin.Address')),
                ('cards', models.ManyToManyField(to='jammin.Card')),
                ('cart', models.ManyToManyField(through='jammin.CartHas', to='jammin.Cart')),
                ('store', models.ManyToManyField(through='jammin.Sells', to='jammin.Item')),
            ],
        ),
        migrations.AddField(
            model_name='sells',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jammin.UserAccount'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderid', models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)])),
                ('date_placed', models.DateField(auto_now_add=True)),
                ('complete', models.BooleanField(default='False')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jammin.Address')),
                ('card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jammin.Card')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jammin.Cart')),
                ('delivery', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jammin.Delivery')),
                ('shipping', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jammin.Shipping')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jammin.UserAccount'),
        ),
        migrations.CreateModel(
            name='EmployeeAccount',
            fields=[
                ('employeeid', models.AutoField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(999999999)])),
                ('salary', models.DecimalField(decimal_places=2, max_digits=11, null=True)),
                ('wage', models.DecimalField(decimal_places=2, max_digits=11, null=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('subordinates', models.ManyToManyField(related_name='_employeeaccount_subordinates_+', to='jammin.EmployeeAccount')),
                ('supervisors', models.ManyToManyField(related_name='_employeeaccount_supervisors_+', to='jammin.EmployeeAccount')),
            ],
        ),
        migrations.AddField(
            model_name='carthas',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jammin.Item'),
        ),
        migrations.AddField(
            model_name='carthas',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jammin.Sells'),
        ),
        migrations.AddField(
            model_name='carthas',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jammin.UserAccount'),
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_has',
            field=models.ManyToManyField(through='jammin.CartHas', to='jammin.Sells'),
        ),
    ]
