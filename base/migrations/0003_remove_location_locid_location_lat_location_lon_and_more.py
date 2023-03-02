# Generated by Django 4.1.5 on 2023-02-26 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_location"),
    ]

    operations = [
        migrations.RemoveField(model_name="location", name="locid",),
        migrations.AddField(
            model_name="location",
            name="lat",
            field=models.CharField(default="2", max_length=40),
        ),
        migrations.AddField(
            model_name="location",
            name="lon",
            field=models.CharField(default="3", max_length=40),
        ),
        migrations.AlterField(
            model_name="location", name="image", field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name="location", name="price", field=models.CharField(max_length=200),
        ),
    ]
