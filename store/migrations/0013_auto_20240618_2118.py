# Generated by Django 3.1.3 on 2024-06-19 01:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0012_auto_20210328_1055'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoreBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
            ],
        ),
        migrations.RenameField(
            model_name='book',
            old_name='Authors',
            new_name='authors',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='Title',
            new_name='image_link',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='Link',
            new_name='link',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='imageLink',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='inventory',
            old_name='Book',
            new_name='book',
        ),
        migrations.RenameField(
            model_name='store',
            old_name='Title',
            new_name='title',
        ),
        migrations.AlterField(
            model_name='store',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='storeBooks',
        ),
        migrations.AddField(
            model_name='storebook',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_books', to='store.book'),
        ),
        migrations.AddField(
            model_name='storebook',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='store_books', to='store.store'),
        ),
    ]
