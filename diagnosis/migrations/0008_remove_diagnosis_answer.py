# Generated by Django 2.1.7 on 2019-03-19 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0007_auto_20190320_0208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='diagnosis',
            name='answer',
        ),
    ]
