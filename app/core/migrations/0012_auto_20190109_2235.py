# Generated by Django 2.1.5 on 2019-01-09 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20190109_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='lat',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='work',
            name='long',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
    ]