# Generated by Django 4.2.5 on 2023-10-04 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('audiobooks', '0005_audiobooks_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingAudiobooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('short_description', models.TextField(max_length=1200)),
                ('audio_book', models.FileField(upload_to='audio')),
                ('book_img', models.ImageField(upload_to='book_img')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_pending', to=settings.AUTH_USER_MODEL)),
                ('genres', models.ManyToManyField(to='audiobooks.genre')),
            ],
        ),
    ]
