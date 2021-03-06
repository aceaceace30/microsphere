# Generated by Django 2.2.4 on 2019-09-01 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20190901_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preventivemaintenance',
            name='actual_date',
            field=models.DateField(help_text='mm/dd/yyyy'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
