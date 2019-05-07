# Generated by Django 2.2 on 2019-05-06 21:18

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20190425_2106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Migration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='entity',
            name='migration',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='entity', to='core.Migration'),
        ),
    ]