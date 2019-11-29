# Generated by Django 2.0.13 on 2019-11-29 07:46

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CreateRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('root_name', models.TextField()),
                ('json_data', jsonfield.fields.JSONField()),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]