# Generated by Django 4.2.5 on 2023-09-22 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_defaultuser_avatar_img_alter_myuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=55, verbose_name='username'),
        ),
    ]
