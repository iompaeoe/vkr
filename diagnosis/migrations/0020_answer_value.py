# Generated by Django 2.1.7 on 2019-04-15 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0019_auto_20190415_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='value',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
    ]
