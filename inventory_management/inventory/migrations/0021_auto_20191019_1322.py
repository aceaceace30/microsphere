# Generated by Django 2.2.4 on 2019-10-19 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_auto_20191010_1552'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='preventivemaintenance',
            options={'ordering': ['-created_at'], 'permissions': [('can_view_pm_list', 'Can view pm list'), ('can_view_units_per_pm', 'Can view units per pm'), ('can_mark_as_done', 'Can mark as done per pm'), ('can_soft_delete_pm', 'Can soft delete pm')]},
        ),
    ]
