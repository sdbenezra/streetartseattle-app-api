# Generated by Django 2.1.4 on 2019-01-03 05:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_work_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='about',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='work',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='work',
            name='category',
            field=models.ManyToManyField(blank=True, to='core.Category'),
        ),
        migrations.AddField(
            model_name='work',
            name='date',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='work',
            name='lat',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='work',
            name='location',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='work',
            name='long',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='work',
            name='measurements',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='work',
            name='media',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='work',
            name='tags',
            field=models.ManyToManyField(blank=True, to='core.Tag'),
        ),
        migrations.AddField(
            model_name='work',
            name='title',
            field=models.CharField(default='Untitled Work', max_length=255),
        ),
        migrations.AddField(
            model_name='work',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='work',
            name='artist',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
