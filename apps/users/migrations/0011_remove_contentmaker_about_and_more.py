# Generated by Django 4.2.5 on 2023-09-30 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_contentmaker_is_approved_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentmaker',
            name='about',
        ),
        migrations.RemoveField(
            model_name='contentmaker',
            name='avatar_img',
        ),
    ]
