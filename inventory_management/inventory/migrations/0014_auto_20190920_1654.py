# Generated by Django 2.2.4 on 2019-09-20 16:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_auto_20190920_1626'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pmunithistory',
            options={'permissions': [('can_add_remarks_per_pm', 'Can add extra remarks per pm')]},
        ),
        migrations.AlterModelOptions(
            name='preventivemaintenance',
            options={'permissions': [('can_view_units_per_pm', 'Can view units per pm')]},
        ),
    ]