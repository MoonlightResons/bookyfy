# Generated by Django 4.2.5 on 2023-09-27 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audiobooks', '0004_delete_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiobooks',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
