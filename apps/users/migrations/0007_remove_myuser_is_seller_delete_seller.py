# Generated by Django 4.2.5 on 2023-09-26 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_myuser_groups_alter_myuser_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='is_Seller',
        ),
        migrations.DeleteModel(
            name='Seller',
        ),
    ]