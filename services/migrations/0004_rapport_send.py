# Generated by Django 4.0.3 on 2022-05-19 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_alter_rapport_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='rapport',
            name='send',
            field=models.BooleanField(default=False),
        ),
    ]
