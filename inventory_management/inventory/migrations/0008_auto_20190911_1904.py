# Generated by Django 2.2.4 on 2019-09-11 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_pmhistoryperunit'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PmHistoryPerUnit',
            new_name='PmUnitHistory',
        ),
    ]
