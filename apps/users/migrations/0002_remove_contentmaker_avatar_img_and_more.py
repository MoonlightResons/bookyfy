# Generated by Django 4.2.5 on 2023-09-17 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentmaker',
            name='avatar_img',
        ),
        migrations.RemoveField(
            model_name='defaultuser',
            name='email_verify',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='avatar_img',
        ),
        migrations.AlterField(
            model_name='defaultuser',
            name='avatar_img',
            field=models.ImageField(default='default-avatar.jpg', null=True, upload_to='avatars'),
        ),
    ]
