# Generated by Django 5.0.6 on 2024-07-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='default\\user.png', upload_to='users/%Y/%m/%d/', verbose_name='Фотография'),
        ),
    ]