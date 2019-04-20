# Generated by Django 2.1.7 on 2019-04-15 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0020_answer_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosis',
            name='inquirer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='diagnosis.Inquirer'),
        ),
        migrations.AddField(
            model_name='inquirer',
            name='description',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
