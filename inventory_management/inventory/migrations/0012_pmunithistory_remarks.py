# Generated by Django 2.2.4 on 2019-09-16 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_auto_20190916_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='pmunithistory',
            name='remarks',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]