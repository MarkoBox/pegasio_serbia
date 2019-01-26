# Generated by Django 2.1.5 on 2019-01-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Reviewer'), (2, 'Preparer'), (3, 'Accountant')], null=True),
        ),
    ]
