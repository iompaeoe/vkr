# Generated by Django 2.1.7 on 2019-04-15 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0022_auto_20190416_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnosis.Question', unique=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnosis.Question'),
        ),
    ]
