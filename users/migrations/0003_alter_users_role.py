# Generated by Django 4.0.3 on 2022-05-21 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='role',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='users.role'),
        ),
    ]
