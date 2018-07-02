"""Basic tasks."""
from __future__ import absolute_import

import logging
import os
import subprocess

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

log = logging.getLogger(__name__)

PRODUCTION_DOMAIN = getattr(settings, 'PRODUCTION_DOMAIN')
DOCS_ITALIA_CONVERSION_UPLOAD_PATH = os.path.join(settings.MEDIA_URL, 'tmp')
DOCS_ITALIA_CONVERTER_EMAIL = getattr(settings, 'DOCS_ITALIA_CONVERTER_EMAIL', 'info@example.org')


@shared_task(queue='web')
def process_file(email, saved, unique_key):
    """
    This celery task save the uploaded file from memory to the
    tmp folder and calls the `pandoc` command on it.
    Than emails the user with the link to download the converted file.

    :param email: the user email
    :param saved: the full path of the uploaded file
    :param unique_key: the unique name of the new folder
    """
    file_path, file_name = os.path.split(saved)
    new_file_name = os.path.splitext(os.path.basename(file_name))[0] + '.rst'
    log.info('Processing uploaded file {} from {}'.format(saved, email))
    err_msg = None
    out_msg = None
    try:
        out_msg = subprocess.check_output(['pandoc', saved], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        err_msg = e.output
    msg = 'http://{}{}/{}/{}'.format(
        PRODUCTION_DOMAIN, DOCS_ITALIA_CONVERSION_UPLOAD_PATH,
        unique_key,
        new_file_name
    )
    if err_msg:
        log.error('There was an error processing %s: %s %s' % (saved, out_msg, err_msg))
    send_mail(
        'Conversione documento di DOCS ITALIA',
        msg,
        DOCS_ITALIA_CONVERTER_EMAIL,
        [email],
        fail_silently=False,
    )
