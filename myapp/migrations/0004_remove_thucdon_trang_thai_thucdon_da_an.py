# Generated by Django 4.2.8 on 2025-05-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_remove_phientrochuyen_nguoi_dung_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thucdon',
            name='trang_thai',
        ),
        migrations.AddField(
            model_name='thucdon',
            name='da_an',
            field=models.BooleanField(default=False),
        ),
    ]
