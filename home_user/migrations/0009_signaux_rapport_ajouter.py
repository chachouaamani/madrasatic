# Generated by Django 4.0.3 on 2022-06-12 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_user', '0008_remove_signaux_archivé_rapport'),
    ]

    operations = [
        migrations.AddField(
            model_name='signaux',
            name='rapport_ajouter',
            field=models.BooleanField(default=False),
        ),
    ]
