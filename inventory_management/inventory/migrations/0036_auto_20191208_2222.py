# Generated by Django 2.2.4 on 2019-12-08 22:22

from django.db import migrations, models
import inventory.models
import inventory.validators


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0035_preventivemaintenance_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preventivemaintenance',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to=inventory.models.update_filename, validators=[inventory.validators.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='preventivemaintenance',
            name='pm_done',
            field=models.NullBooleanField(),
        ),
    ]
