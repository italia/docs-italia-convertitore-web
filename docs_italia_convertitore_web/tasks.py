"""Basic tasks."""
from __future__ import absolute_import
import logging

from base64 import urlsafe_b64encode
import os
import subprocess
import shutil

from django.core.files.storage import default_storage
from django.conf import settings
from django.core.mail import send_mail

from readthedocs.worker import app

log = logging.getLogger(__name__)

CONVERSION_UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, 'tmp')


@app.task(queue='web')
def process_file(email, uploaded):
    """
    This celery task save the uploaded file from memory to the
    tmp folder and calls the `converti` command on it.
    Than emails the user with the link to download the converted file.
    """
    unique_key = urlsafe_b64encode(email + uploaded.name).rstrip('=')# maybe we should use date time now to allow the uploado of a file with the same name
    new_folder_name = os.path.join(CONVERSION_UPLOAD_DIR, unique_key)
    if not os.path.exists(new_folder_name):
        os.mkdir(new_folder_name)
    file_path = os.path.join(new_folder_name, uploaded.name)
    saved = os.path.join(CONVERSION_UPLOAD_DIR, new_folder_name, uploaded.name)
    with default_storage.open(saved, 'wb+') as destination:
        for chunk in uploaded.chunks():
            destination.write(chunk)
    subprocess.call(['converti',  saved], cwd=new_folder_name)
    zipped_name = os.path.splitext(uploaded.name)[0]
    shutil.make_archive( #  create the archive
        os.path.join(new_folder_name, zipped_name),
        'zip',
        os.path.join(new_folder_name,'risultato-conversione')
    )
    log.info('Processing uploaded file {} from {}'.format(uploaded.name, email))
    send_mail(
        'Conversione del documento effettuata!',
        'http://localhost:8000/media/tmp/{}/{}.zip'.format(unique_key, zipped_name),
        'from@example.com',
        [email],
        fail_silently=False,
    )
