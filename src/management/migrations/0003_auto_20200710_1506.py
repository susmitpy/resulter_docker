# Generated by Django 3.0.7 on 2020-07-10 09:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20200710_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='assessmentlog',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
        migrations.AddField(
            model_name='assessmentlog',
            name='new_marks',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='assessmentlog',
            name='old_marks',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='assessmentlog',
            name='updated_by',
            field=models.CharField(default='ADMIN', max_length=20),
        ),
        migrations.AddField(
            model_name='pt_evs_assessmentlog',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.localtime),
        ),
        migrations.AddField(
            model_name='pt_evs_assessmentlog',
            name='new_marks',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pt_evs_assessmentlog',
            name='old_marks',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pt_evs_assessmentlog',
            name='updated_by',
            field=models.CharField(default='ADMIN', max_length=20),
        ),
    ]