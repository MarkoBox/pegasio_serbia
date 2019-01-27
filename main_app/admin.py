from django.contrib import admin
from .models import Clients, Batches, Pieces, BatchTracking
from import_export.admin import ImportExportActionModelAdmin
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

import zipfile
import os
from main_app.InMemoryZip import InMemoryZipFile


@admin.register(Clients)
class ClientsAdmin(ImportExportActionModelAdmin):
    list_display = ['name', 'vat', 'period_from', 'period_to', 'path_grps', 'path_alfresco', 'chr_flag',
                    'e_comerce_flag']


def generate_pieces(modeladmin, request, queryset):
    """Function to read uploaded zip file and file table pieces with file names and paths"""
    for batch in queryset:
        batch_zip = zipfile.ZipFile(batch.file_sent_to_accountant)
        for file_name in batch_zip.namelist():
            file_info = batch_zip.getinfo(file_name)
            if file_info.is_dir():
                pass
            else:
                # otvaram ZipExtFile
                zipextfile = batch_zip.open(file_info, mode='r')
                # moram da koristim ovu klasu jer ona ima read metodu koju zahteva filefield
                unziped_file = ContentFile(zipextfile.read(), name=file_name)
                # naziv fajla je malo rogobatan ali nema veze
                Pieces.objects.get_or_create(file=unziped_file, file_name=os.path.basename(file_name),
                                             folder_original=os.path.dirname(file_name),
                                             batch=batch)
                # chekiraj da je batch generisan
                Batches.objects.filter(pk=batch.id).update(pieces_generated=True)


generate_pieces.short_description = 'Generate Pieces'


def generate_codified_batch(modeladmin, request, queryset):
    """Function to create folder and file structure and zip it"""
    for batch in queryset:
        pieces = Pieces.objects.filter(batch=batch)
        mem_zip = InMemoryZipFile(file_name=batch.name)
        for piece in pieces:
            in_file = open(piece.file.path, 'rb')
            data = in_file.read()
            mem_zip.append(filename_in_zip=f'/{piece.folder_assigned}/{piece.period}/{piece.codification}\
            .{piece.file_name.rsplit(".")[-1]}'
                           , file_contents=data)
            in_file.close()
        data = mem_zip.data
        files_codified = SimpleUploadedFile.from_dict(
            {'content': data, 'filename': batch.name + '.zip', 'content-type': 'application/zip'})
        obj = Batches.objects.get(pk=batch.id)
        obj.file_codified = files_codified
        obj.save()


generate_codified_batch.short_description = 'Generate Codified Batch'


@admin.register(Batches)
class BatchesAdmin(ImportExportActionModelAdmin):
    list_display = ['name', 'period', 'file_sent_to_accountant', 'accountant_name', 'file_codified', 'gl_export',
                    'client_name', 'date_time_uploaded']
    actions = [generate_pieces, generate_codified_batch]


@admin.register(Pieces)
class PiecesAdmin(ImportExportActionModelAdmin):
    list_display = ['file', 'file_name', 'folder_original', 'codification', 'period', 'folder_assigned', 'booked',
                    'batch',
                    'get_client']
    list_editable = ['codification', 'period', 'folder_assigned', 'booked']
    list_filter = ['batch', 'folder_original', 'folder_assigned', 'batch__client_name']
    save_as = True

    def get_client(self, obj):
        return obj.batch.client_name

    get_client.admin_order_field = 'client'
    get_client.short_description = 'Client'


@admin.register(BatchTracking)
class BatchTrackingAdmin(ImportExportActionModelAdmin):
    list_display = ['sent_to_accountant', 'archived_sent_batch',
                    'booked_and_codified', 'controlled', 'sent_back_to_accountant', 'archived_to_alfresco',
                    'archived_to_grps', 'archived_of_gl_export', 'batch']
