# Generated by Django 2.2 on 2019-04-22 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190422_1722'),
    ]

    operations = [
        migrations.AddField(
            model_name='entitymap',
            name='name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
