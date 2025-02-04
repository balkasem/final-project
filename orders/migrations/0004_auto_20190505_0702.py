# Generated by Django 2.2 on 2019-05-05 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0003_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='category',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='diffrentWithSize',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='isPizza',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='priceBig',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='toppingCount',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='isPizza',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='size',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='toppingCount',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='toppings',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='tel',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
