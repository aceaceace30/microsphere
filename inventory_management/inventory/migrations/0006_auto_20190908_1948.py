# Generated by Django 2.2.4 on 2019-09-08 19:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import inventory.validators
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0005_auto_20190906_1450'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPreventiveMaintenance',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('service_report_number', models.CharField(db_index=True, max_length=255)),
                ('target_date', models.DateField()),
                ('target_time', models.TimeField()),
                ('actual_date', models.DateField()),
                ('pm_date_done', models.DateField(blank=True, null=True)),
                ('pm_done', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('Covered by MA', 'Covered by MA'), ('Not Covered by MA', 'Not Covered by MA')], max_length=100)),
                ('remarks', models.TextField(blank=True, max_length=500, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('business_unit', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.BusinessUnit')),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical preventive maintenance',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalUnit',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('serial_number', models.CharField(db_index=True, max_length=15, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Please enter alphanumeric characters.')])),
                ('computer_tag', models.CharField(db_index=True, max_length=10, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', 'Please enter alphanumeric characters.')])),
                ('mst_tag', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.CharField(max_length=255)),
                ('designation', models.CharField(max_length=255)),
                ('host_name', models.CharField(blank=True, max_length=255, null=True)),
                ('mac_address', models.CharField(blank=True, max_length=17, null=True, validators=[inventory.validators.validate_mac_address])),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('monitor_type', models.CharField(blank=True, choices=[('LCD', 'LCD'), ('CRT', 'CRT')], max_length=10, null=True)),
                ('monitor_size', models.PositiveIntegerField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, max_length=500, null=True)),
                ('active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('business_unit', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.BusinessUnit')),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('hdd_size', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.HddSize')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('machine_brand', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.Brand')),
                ('machine_type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.MachineType')),
                ('model', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.Model')),
                ('monitor_brand', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.Brand')),
                ('office_application', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.OfficeApplication')),
                ('operating_system', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.OperatingSystem')),
                ('processor', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.Processor')),
                ('total_ram', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='inventory.TotalRam')),
                ('updated_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical unit',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.DeleteModel(
            name='UnitRemarks',
        ),
    ]
