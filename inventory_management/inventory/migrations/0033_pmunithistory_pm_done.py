# Generated by Django 2.2.4 on 2019-12-07 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0032_auto_20191206_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='pmunithistory',
            name='pm_done',
            field=models.BooleanField(default=False),
        ),
    ]