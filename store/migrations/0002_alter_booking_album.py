# Generated by Django 3.2.7 on 2021-09-22 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.album'),
        ),
    ]
