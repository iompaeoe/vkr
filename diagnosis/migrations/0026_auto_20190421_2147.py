# Generated by Django 2.1.7 on 2019-04-21 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0025_inquirer_ann_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inquirer',
            name='ANN_model',
            field=models.FileField(upload_to=''),
        ),
    ]
