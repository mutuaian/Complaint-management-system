# Generated by Django 2.2.1 on 2019-06-22 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0020_remove_complaints_remark'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaints',
            name='complaint_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]