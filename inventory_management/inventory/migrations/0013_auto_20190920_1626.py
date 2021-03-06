# Generated by Django 2.2.4 on 2019-09-20 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0012_pmunithistory_remarks'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='unit',
            options={'permissions': [('can_view_unit_list', 'Can view unit list'), ('can_soft_delete_unit', 'Can soft delete unit'), ('can_view_unit_history', 'Can view unit history')]},
        ),
        migrations.AlterField(
            model_name='historicalpreventivemaintenance',
            name='service_report_number',
            field=models.CharField(db_index=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='preventivemaintenance',
            name='service_report_number',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
