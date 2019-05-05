# Generated by Django 2.2 on 2019-05-05 00:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jammin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='CartHas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('cart', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='jammin.Cart')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jammin.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jammin.UserAccount')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_has',
            field=models.ManyToManyField(through='jammin.CartHas', to='jammin.Item'),
        ),
        migrations.AddField(
            model_name='useraccount',
            name='cart',
            field=models.ManyToManyField(through='jammin.CartHas', to='jammin.Cart'),
        ),
    ]
