# Generated by Django 4.0.3 on 2022-03-23 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_users_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
    ]