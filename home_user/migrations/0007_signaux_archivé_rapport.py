# Generated by Django 4.0.3 on 2022-06-12 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_user', '0006_alter_notifications_from_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='signaux_archivé',
            name='rapport',
            field=models.IntegerField(default=0),
        ),
    ]
