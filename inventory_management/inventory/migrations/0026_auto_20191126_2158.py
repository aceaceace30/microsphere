# Generated by Django 2.2.4 on 2019-11-26 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0025_auto_20191124_2303'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='businessunit',
            options={'ordering': ['business_unit_name']},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'ordering': ['-created_at'], 'permissions': [('can_view_unit_list', 'Can view unit list'), ('can_soft_delete_unit', 'Can soft delete unit'), ('can_view_unit_history', 'Can view unit history')]},
        ),
        migrations.AddField(
            model_name='historicalunit',
            name='working',
            field=models.CharField(choices=[('Y', 'Y'), ('N', 'N')], default='Y', max_length=1),
        ),
        migrations.AddField(
            model_name='unit',
            name='working',
            field=models.CharField(choices=[('Y', 'Y'), ('N', 'N')], default='Y', max_length=1),
        ),
        migrations.AlterField(
            model_name='businessunit',
            name='area',
            field=models.CharField(choices=[('', '--------'), ('Provincial', 'Provincial'), ('Metro Manila', 'Metro Manila'), ('Head Office', 'Head Office')], max_length=50),
        ),
        migrations.AlterField(
            model_name='historicalunit',
            name='area',
            field=models.CharField(choices=[('', '--------'), ('Provincial', 'Provincial'), ('Metro Manila', 'Metro Manila'), ('Head Office', 'Head Office')], max_length=50),
        ),
        migrations.AlterField(
            model_name='unit',
            name='area',
            field=models.CharField(choices=[('', '--------'), ('Provincial', 'Provincial'), ('Metro Manila', 'Metro Manila'), ('Head Office', 'Head Office')], max_length=50),
        ),
    ]
