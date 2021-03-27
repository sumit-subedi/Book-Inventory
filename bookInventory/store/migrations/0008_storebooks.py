# Generated by Django 3.1.3 on 2021-03-26 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20210326_1717'),
    ]

    operations = [
        migrations.CreateModel(
            name='storeBooks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('Book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='store.book')),
                ('Store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.store')),
            ],
        ),
    ]
