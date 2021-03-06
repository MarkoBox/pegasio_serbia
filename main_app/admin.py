from django.contrib import admin
from .models import Clients, Batches, Pieces, BatchTracking, FolderChoises
from import_export.admin import ImportExportActionModelAdmin
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile

import zipfile
import os
from main_app.InMemoryZip import InMemoryZipFile

admin.site.site_header = 'Pegasio Serbia'  # default: "Django Administration"
admin.site.index_title = 'Pegasio Serbia'  # default: "Site administration"
admin.site.site_title = 'Pegasio Serbia'  # default: "Django site admin"


class PiecesInLine(admin.TabularInline):
    model = Pieces
    readonly_fields = ('file', 'file_name', 'folder_original',)
    can_delete = False


@admin.register(Clients)
class ClientsAdmin(ImportExportActionModelAdmin):
    list_display = ['name', 'alternative_name', 'vat', 'period_from', 'period_to', 'path_grps', 'path_alfresco',
                    'chr_flag', 'e_comerce_flag']


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
                BatchTracking.objects.filter(pk=batch.id).update(pieces_generated=True)


generate_pieces.short_description = 'Generate Pieces'


def generate_codified_batch(modeladmin, request, queryset):
    """Function to create folder and file structure and zip it"""
    for batch in queryset:
        pieces = Pieces.objects.filter(batch=batch)
        mem_zip = InMemoryZipFile(file_name=batch.batch_name)
        for piece in pieces:
            in_file = open(piece.file.path, 'rb')
            data = in_file.read()
            # moze li ovo bolje
            if piece.codification is None:
                filename_in_zip = f'/{piece.folder_assigned}/{piece.folder_month}/{piece.file_name}'
            else:
                filename_in_zip = f'/{piece.folder_assigned}/{piece.folder_month}/{piece.codification}.{piece.file_name.rsplit(".")[-1]}'
            mem_zip.append(filename_in_zip=filename_in_zip, file_contents=data)
            in_file.close()
        data = mem_zip.data
        files_codified = SimpleUploadedFile.from_dict({'content': data, 'filename': batch.batch_name + '.zip', 'content-type': 'application/zip'})
        obj = Batches.objects.get(pk=batch.id)
        obj.file_codified = files_codified
        obj.save()
        # chekiraj da je batch proknjizen i kodifikovan
        BatchTracking.objects.filter(pk=batch.id).update(booked_and_codified=True)


generate_codified_batch.short_description = 'Generate Codified Batch'


@admin.register(Batches)
class BatchesAdmin(ImportExportActionModelAdmin):
    list_display = ['batch_name', 'month_year', 'file_sent_to_accountant', 'accountant_name', 'file_codified',
                    'gl_export',
                    'client_name', 'date_time_uploaded']
    actions = [generate_pieces, generate_codified_batch]
    inlines = [PiecesInLine]


@admin.register(Pieces)
class PiecesAdmin(ImportExportActionModelAdmin):
    list_display = ['file', 'file_name', 'folder_original', 'codification', 'folder_month', 'folder_assigned', 'booked',
                    'comment',
                    'batch', ]
    list_editable = ['codification', 'folder_month', 'folder_assigned', 'booked', 'comment']
    list_filter = ['batch', 'folder_original', 'folder_assigned', 'batch__client_name']
    list_display_links = ['file_name']
    save_as = True
    save_on_top = True

    def get_client(self, obj):
        return obj.batch.client_name

    get_client.admin_order_field = 'client'
    get_client.short_description = 'Client'


@admin.register(BatchTracking)
class BatchTrackingAdmin(ImportExportActionModelAdmin):
    list_display = ['archived_sent_batch',
                    'booked_and_codified', 'controlled', 'sent_back_to_accountant', 'archived_to_alfresco',
                    'archived_to_grps', 'archived_of_gl_export', 'batch']


@admin.register(FolderChoises)
class FolderChoisesAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'folder_name']
    list_editable = ['folder_name']
