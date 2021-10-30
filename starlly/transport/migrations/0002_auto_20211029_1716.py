# Generated by Django 2.2.15 on 2021-10-29 17:16

from django.db import migrations, models
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('transport', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permittracker',
            name='Alerts',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Alerts'),
        ),
        migrations.AlterField(
            model_name='permittracker',
            name='Destination',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Destination'),
        ),
        migrations.AlterField(
            model_name='permittracker',
            name='ILMS_number',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='ILMS Number'),
        ),
        migrations.AlterField(
            model_name='permittracker',
            name='LoadingLocation',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Loading Location'),
        ),
        migrations.AlterField(
            model_name='permittracker',
            name='PermitNumber',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Permit Number'),
        ),
        migrations.AlterField(
            model_name='permittracker',
            name='PermitStart',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Permit Start'),
        ),
        migrations.AlterField(
            model_name='permittracker',
            name='PermitValidTill',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Permit Valid Till'),
        ),
        migrations.AlterField(
            model_name='permittracker',
            name='Qty',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Qty'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='capacity',
            field=models.FloatField(default=0, null=True, verbose_name='Capacity '),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='gpsIMEI',
            field=models.IntegerField(null=True, verbose_name='GPS IMEI'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='installationtype',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='New Installation', max_length=100, no_check_for_status=True, verbose_name='Installation Type'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='licenseEnd',
            field=models.DateTimeField(blank=True, null=True, verbose_name='License End Date'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='licenseStart',
            field=models.DateTimeField(blank=True, null=True, verbose_name='License Start Date'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='licenseStatus',
            field=models.CharField(max_length=30, null=True, verbose_name='License Status'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='ownerPhone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Owner Phone '),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='registrationBy',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Registration By'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='registrationDate',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Registration Date'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='simNo',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Sim No'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='telecomProvider',
            field=models.CharField(max_length=30, null=True, verbose_name='Telecom Provider'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='totalPermits',
            field=models.IntegerField(default=0, null=True, verbose_name='Total Permits'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicleGroup',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='DMG', max_length=100, no_check_for_status=True, verbose_name='Vehicle Group '),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicleNumber',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Vehicle Number'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicleStatus',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Vehicle Status '),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicleType',
            field=model_utils.fields.StatusField(choices=[(0, 'dummy')], default='Tipper', max_length=100, no_check_for_status=True, verbose_name='Vehicle Type'),
        ),
    ]