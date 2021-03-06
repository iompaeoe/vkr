# Generated by Django 2.1.7 on 2019-04-15 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0016_auto_20190415_1504'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inquirer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialityInquirer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inquirer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnosis.Inquirer')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnosis.Specialty')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='specialityinquirer',
            unique_together={('specialty', 'inquirer')},
        ),
    ]
