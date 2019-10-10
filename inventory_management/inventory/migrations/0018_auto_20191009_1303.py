# Generated by Django 2.2.4 on 2019-10-09 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_auto_20190923_1138'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalunit',
            name='area',
            field=models.CharField(choices=[('Provincial', 'Provincial'), ('Metro Manila', 'Metro Manila'), ('Head Office', 'Head Office')], default='Provincial', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unit',
            name='area',
            field=models.CharField(choices=[('Provincial', 'Provincial'), ('Metro Manila', 'Metro Manila'), ('Head Office', 'Head Office')], default='Provincial', max_length=50),
            preserve_default=False,
        ),
    ]
