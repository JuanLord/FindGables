# Generated by Django 4.1.7 on 2023-03-01 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0005_alter_location_lat_alter_location_lon"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="location",
            name="id",
        ),
        migrations.AlterField(
            model_name="location",
            name="name",
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]