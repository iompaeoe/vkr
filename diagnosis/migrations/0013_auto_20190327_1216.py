# Generated by Django 2.1.7 on 2019-03-27 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0012_auto_20190327_1207'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diagnosis',
            old_name='answer',
            new_name='question',
        ),
        migrations.RemoveField(
            model_name='question',
            name='answer',
        ),
        migrations.AddField(
            model_name='question',
            name='answer',
            field=models.ManyToManyField(to='diagnosis.Answer'),
        ),
    ]
