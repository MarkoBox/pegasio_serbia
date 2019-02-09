from django.db import models
from pegasio_serbia.users.models import User


class Clients(models.Model):
    name = models.CharField(max_length=255, unique=True)
    alternative_name = models.CharField(max_length=255, null=True, blank=True)
    period_from = models.DateField()
    period_to = models.DateField()
    path_grps = models.CharField(max_length=255, null=True, blank=True)
    path_alfresco = models.CharField(max_length=255, null=True, blank=True)
    chr_flag = models.BooleanField(verbose_name='CHR')
    e_comerce_flag = models.BooleanField(verbose_name='E commerce')
    vat = models.CharField(max_length=20, null=True, blank=True, verbose_name='VAT date')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'client'
        verbose_name_plural = 'clients'


class Batches(models.Model):
    # name treba da bude kalkulativno polje
    # name = models.CharField(max_length=255)
    number = models.IntegerField(unique=True)
    month_year = models.CharField(max_length=20, null=True, blank=True, verbose_name='MonthYear')
    date_time_uploaded = models.DateTimeField(auto_now_add=True)
    file_sent_to_accountant = models.FileField(null=True, blank=True, upload_to='files_sent/')
    file_codified = models.FileField(null=True, blank=True, upload_to='files_codified/')
    gl_export = models.FileField(null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    accountant_name = models.ForeignKey(User, on_delete=models.PROTECT)
    client_name = models.ForeignKey(Clients, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.batch_name}'

    def _get_batch_name(self):
        """Return batch name"""
        return f"B-{self.number} {self.month_year} {self.client_name}"

    batch_name = property(_get_batch_name)

    class Meta:
        verbose_name = 'batch'
        verbose_name_plural = 'batches'


def piece_upload_path(instance, filename):
    return f'pieces/{instance.batch.batch_name}/{filename}'


class Pieces(models.Model):
    ACHATS = 'Achats'
    BANQUE = 'Banque'
    VENTES = 'Ventes'
    CAISSE = 'Caisse'
    OD = 'OD'
    REJECTS = 'Rejects'
    INCOMPLETE = 'Incomplete'
    DOUBLONS = 'Doublons'
    GED = 'Ged'
    FORWARDED = 'Forwarded'
    # dodaj ostale
    FOLDER_CHOISES = (
        (ACHATS, 'Achats'),
        (BANQUE, 'Banque'),
        (VENTES, 'Ventes'),
        (CAISSE, 'Caisse'),
        (OD, 'OD'),
        (REJECTS, 'Rejects'),
        (INCOMPLETE, 'Incomplete'),
        (DOUBLONS, 'Doublons'),
        (GED, 'Ged'),
        (FORWARDED, 'Forwarded')
    )
    # dodaj regex validatore na codification polje i period polje
    file = models.FileField(null=True, blank=True, upload_to=piece_upload_path)
    file_name = models.CharField(max_length=255)
    folder_original = models.CharField(max_length=255, null=True, blank=True)
    codification = models.CharField(max_length=255, null=True, blank=True)
    folder_month = models.CharField(max_length=255, null=True, blank=True)
    folder_assigned = models.CharField(max_length=255, choices=FOLDER_CHOISES, null=True,
                                       blank=True)
    booked = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, null=True, blank=True)
    batch = models.ForeignKey(Batches, on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['folder_original', 'file_name', 'batch']
        verbose_name = 'piece'
        verbose_name_plural = 'pieces'


class BatchTracking(models.Model):
    reviewer = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT,
                                 related_name='reviewers_batches')
    preparer = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT,
                                 related_name='preparers_batches')
    pieces_generated = models.BooleanField(default=False)
    accountant_notified = models.BooleanField(default=False)
    archived_sent_batch = models.BooleanField(default=False)
    booked_and_codified = models.BooleanField(default=False)
    controlled = models.BooleanField(default=False)
    sent_back_to_accountant = models.BooleanField(default=False)
    archived_to_alfresco = models.BooleanField(default=False)
    archived_to_grps = models.BooleanField(default=False)
    archived_of_gl_export = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, null=True, blank=True)
    batch = models.OneToOneField(Batches, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.batch.batch_name

    class Meta:
        verbose_name = 'batch tracking'
        verbose_name_plural = 'batch tracking'
