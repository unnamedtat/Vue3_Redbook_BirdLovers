# Generated by Django 5.1.3 on 2024-12-05 13:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Server01", "0012_image_height_image_width"),
    ]

    operations = [
        migrations.AddField(
            model_name="image",
            name="deleteUrl",
            field=models.CharField(default="", max_length=256, verbose_name="删除图片URL"),
        ),
        migrations.AlterField(
            model_name="image",
            name="imagePath",
            field=models.CharField(default="", max_length=256, verbose_name="帖子图片"),
        ),
    ]
