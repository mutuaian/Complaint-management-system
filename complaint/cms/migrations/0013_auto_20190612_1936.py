# Generated by Django 2.2.1 on 2019-06-12 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_auto_20190612_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaints',
            name='complaint_details',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='complaint_type',
            field=models.CharField(max_length=100),
        ),
    ]