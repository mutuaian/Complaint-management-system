# Generated by Django 2.2.1 on 2019-06-12 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0014_auto_20190612_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaints',
            name='status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]