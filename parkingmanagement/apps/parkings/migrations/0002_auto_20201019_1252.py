# Generated by Django 3.1.2 on 2020-10-19 12:52
import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingspot',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(geography=True,
                                                                 help_text='Represented as (longitude, latitude)', srid=4326),
        ),
    ]
