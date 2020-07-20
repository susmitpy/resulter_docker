# Generated by Django 3.0.7 on 2020-07-20 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0009_auto_20200715_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='division',
            field=models.CharField(choices=[('E', 'E')], default='', max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='pt_evs_exam',
            name='division',
            field=models.CharField(choices=[('E', 'E')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='division',
            field=models.CharField(choices=[('E', 'E')], default='', max_length=5, null=True),
        ),
    ]