# Generated by Django 3.1.2 on 2020-10-19 10:41
import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkingSpot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Human readable name/code', max_length=256)),
                ('is_reserved', models.BooleanField(default=False)),
                ('point', django.contrib.gis.db.models.fields.PointField(help_text='Represented as (longitude, latitude)', srid=4326)),
                ('current_base_cost', models.FloatField(help_text='Price for the parking spot per minute')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_time', models.DateTimeField(help_text='from what time this booking is valid.')),
                ('valid_up_to', models.DateTimeField(help_text='till what time this booking is valid.')),
                ('cancled_at', models.DateTimeField(blank=True, help_text='Till what time this booking is valid.', null=True)),
                ('applicable_base_cost', models.FloatField(blank=True, help_text='Cost at which the booking was done.', null=True)),
                ('parking_spot', models.ForeignKey(help_text='Parking Spot for which booking is Created.', on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='parkings.parkingspot')),
                ('tenant', models.ForeignKey(help_text='User for whom booking is Created.', on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]