# Generated by Django 4.2.5 on 2023-09-22 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0004_alter_myuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultuser',
            name='avatar_img',
            field=models.ImageField(default='default-avatar.jpg', null=True, upload_to='avatars'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='groups',
            field=models.ManyToManyField(null=True, related_name='my_users', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(null=True, related_name='my_users', to='auth.permission'),
        ),
    ]