# Generated by Django 2.1.7 on 2019-05-14 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0030_auto_20190430_0327'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquirer',
            name='medical_report_template',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]