# Generated by Django 3.0.3 on 2021-01-11 00:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cws', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordcollection',
            name='word_collection',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z ]*$', 'Word Collection name can only be alphanumeric.')]),
        ),
    ]
