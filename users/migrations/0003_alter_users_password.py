# Generated by Django 4.0.3 on 2022-03-19 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_users_email_alter_users_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=10, null=True),
        ),
    ]