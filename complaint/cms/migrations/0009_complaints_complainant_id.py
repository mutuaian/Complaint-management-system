# Generated by Django 2.2.1 on 2019-06-12 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0008_auto_20190612_0730'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaints',
            name='complainant_id',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='cms.Complainants'),
        ),
    ]