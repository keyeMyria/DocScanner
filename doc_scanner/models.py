from django.db import models as django_models
from djongo import models as djongo_models
from django.urls import reverse
from django import forms


class GoogleAppConfiguration(django_models.Model):
    client_id = djongo_models.CharField(max_length=300)
    project_id = djongo_models.CharField(max_length=300)
    auth_uri = djongo_models.CharField(max_length=300)
    token_uri = djongo_models.CharField(max_length=300)
    auth_provider_x509_cert_url = djongo_models.CharField(max_length=300)
    client_secret = djongo_models.CharField(max_length=300)
    redirect_uris = djongo_models.CharField(max_length=300)
    creation_date = djongo_models.DateTimeField(auto_now_add=True)
    last_updated_date = djongo_models.DateTimeField(auto_now=True)

    objects = djongo_models.DjongoManager()

    def __str__(self):
        return f'GoogleAPI Config'


class Source(django_models.Model):
    GoogleDRIVE = 'google_drive'
    REMOTE = 'remote_system'

    FILE_LOCATION = (
        (GoogleDRIVE, 'Google Drive'),
        (REMOTE, 'Remote System')
    )

    source_type = djongo_models.CharField(max_length=20, choices=FILE_LOCATION, default=GoogleDRIVE)
    source_name = djongo_models.CharField(max_length=100, unique=True, editable=False)
    drive_userId = djongo_models.EmailField(blank=True)
    drive_auth_token = djongo_models.CharField(max_length=300, editable=False, blank=True)
    drive_refresh_token = djongo_models.CharField(max_length=300, editable=False, blank=True)
    drive_access_token = djongo_models.CharField(max_length=300, editable=False, blank=True)
    drive_token_expiry = djongo_models.DateTimeField(editable=False, blank=True)
    remote_systemIP = djongo_models.GenericIPAddressField(blank=True, null=True)
    remote_username = djongo_models.CharField(max_length=100, blank=True)
    remote_password = djongo_models.CharField(max_length=500, blank=True)
    creation_date = djongo_models.DateTimeField(auto_now_add=True)
    last_updated_date = djongo_models.DateTimeField(auto_now=True)

    objects = djongo_models.DjongoManager()

    def __str__(self):
        return f'Source : {self.source_type}_{self.source_name}'

    def get_absolute_url(self):
        return reverse('elibot-scanner-source-detail', kwargs={"pk": self.pk})


class DriveUserInfo(djongo_models.Model):
    user_source = djongo_models.ForeignKey(Source, on_delete=djongo_models.CASCADE)
    user_name = djongo_models.CharField(max_length=300, blank=True)
    user_img_url = djongo_models.URLField(blank=True)
    user_email = djongo_models.EmailField(blank=True)

    def __str__(self):
        return self.user_name


class FileLoc(djongo_models.Model):
    file_address = djongo_models.CharField(max_length=300, blank=True)
    file_mime_type = djongo_models.CharField(max_length=100, blank=True)
    file_name = djongo_models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True


class FileLocForm(forms.ModelForm):
    class Meta:
        model = FileLoc
        fields = ['file_name', 'file_mime_type', 'file_address']


class FilesAddress(djongo_models.Model):

    source = djongo_models.ForeignKey(Source, on_delete=djongo_models.CASCADE)
    file_list = djongo_models.ArrayModelField(
        model_container=FileLoc,
        model_form_class=FileLocForm,
        blank=True
    )
    creation_date = djongo_models.DateTimeField(auto_now_add=True)
    last_updated_date = djongo_models.DateTimeField(auto_now=True)

    objects = djongo_models.DjongoManager()

    def __str__(self):
        return f'Location : {self.source.source_name}'

    def get_absolute_url(self):
        return reverse('elibot-scanner-files-list')

