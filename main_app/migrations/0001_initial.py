# Generated by Django 2.1.5 on 2019-02-10 18:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Batches',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(unique=True)),
                ('month_year', models.CharField(blank=True, max_length=20, null=True, verbose_name='MonthYear')),
                ('date_time_uploaded', models.DateTimeField(auto_now_add=True)),
                ('file_sent_to_accountant', models.FileField(blank=True, null=True, upload_to='files_sent/')),
                ('file_codified', models.FileField(blank=True, null=True, upload_to='files_codified/')),
                ('gl_export', models.FileField(blank=True, null=True, upload_to='')),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'batch',
                'verbose_name_plural': 'batches',
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('alternative_name', models.CharField(blank=True, max_length=255, null=True)),
                ('period_from', models.DateField()),
                ('period_to', models.DateField()),
                ('path_grps', models.CharField(blank=True, max_length=255, null=True)),
                ('path_alfresco', models.CharField(blank=True, max_length=255, null=True)),
                ('chr_flag', models.BooleanField(verbose_name='CHR')),
                ('e_comerce_flag', models.BooleanField(verbose_name='E commerce')),
                ('vat', models.CharField(blank=True, max_length=20, null=True, verbose_name='VAT date')),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
            },
        ),
        migrations.CreateModel(
            name='FolderChoises',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folder_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pieces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to=main_app.models.piece_upload_path)),
                ('file_name', models.CharField(max_length=255)),
                ('folder_original', models.CharField(blank=True, max_length=255, null=True)),
                ('codification', models.CharField(blank=True, max_length=255, null=True)),
                ('folder_month', models.CharField(blank=True, max_length=255, null=True)),
                ('booked', models.BooleanField(default=False)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'piece',
                'verbose_name_plural': 'pieces',
                'ordering': ['folder_original', 'file_name', 'batch'],
            },
        ),
        migrations.CreateModel(
            name='BatchTracking',
            fields=[
                ('pieces_generated', models.BooleanField(default=False)),
                ('accountant_notified', models.BooleanField(default=False)),
                ('archived_sent_batch', models.BooleanField(default=False)),
                ('booked_and_codified', models.BooleanField(default=False)),
                ('controlled', models.BooleanField(default=False)),
                ('sent_back_to_accountant', models.BooleanField(default=False)),
                ('archived_to_alfresco', models.BooleanField(default=False)),
                ('archived_to_grps', models.BooleanField(default=False)),
                ('archived_of_gl_export', models.BooleanField(default=False)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('batch', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main_app.Batches')),
                ('preparer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='preparers_batches', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reviewers_batches', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'batch tracking',
                'verbose_name_plural': 'batch tracking',
            },
        ),
        migrations.AddField(
            model_name='pieces',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Batches'),
        ),
        migrations.AddField(
            model_name='pieces',
            name='folder_assigned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main_app.FolderChoises'),
        ),
        migrations.AddField(
            model_name='batches',
            name='accountant_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='batches',
            name='client_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Clients'),
        ),
    ]
