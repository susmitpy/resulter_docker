# Generated by Django 3.0.7 on 2020-07-10 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='student',
            name='unique_student',
        ),
        migrations.AddField(
            model_name='exam',
            name='division',
            field=models.CharField(choices=[], max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='division',
            field=models.CharField(choices=[], max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='identifier',
            field=models.CharField(blank=True, default='', help_text='LD / VACANT', max_length=8),
        ),
        migrations.AddField(
            model_name='student',
            name='sports',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(to='management.Subject'),
        ),
        migrations.AddConstraint(
            model_name='student',
            constraint=models.UniqueConstraint(fields=('roll_num', 'division'), name='unique_student'),
        ),
    ]
