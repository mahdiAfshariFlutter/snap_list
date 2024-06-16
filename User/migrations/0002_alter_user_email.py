# Generated by Django 5.0.3 on 2024-06-12 18:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=uuid.uuid1, error_messages={'unique': 'این ایمیل تکراری است'}, max_length=254, unique=True),
        ),
    ]