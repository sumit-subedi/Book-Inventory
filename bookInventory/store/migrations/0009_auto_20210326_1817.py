# Generated by Django 3.1.3 on 2021-03-26 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_storebooks'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='Book',
        ),
        migrations.RemoveField(
            model_name='store',
            name='count',
        ),
    ]