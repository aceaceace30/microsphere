# Generated by Django 2.2.4 on 2019-11-24 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0024_auto_20191119_1054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='businessunit',
            options={},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'permissions': [('can_view_unit_list', 'Can view unit list'), ('can_soft_delete_unit', 'Can soft delete unit'), ('can_view_unit_history', 'Can view unit history')]},
        ),
    ]