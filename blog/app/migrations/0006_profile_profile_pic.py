# Generated by Django 5.0.2 on 2024-03-15 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='bg.jpg', null=True, upload_to='images/'),
        ),
    ]