# Generated by Django 5.0.6 on 2024-07-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_product_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(default='default\\game.png', upload_to='games/', verbose_name='Обложка'),
        ),
    ]