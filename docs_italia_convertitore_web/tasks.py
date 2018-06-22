"""Basic tasks."""
from __future__ import absolute_import

import logging
import os
import subprocess

from django.conf import settings
from django.core.mail import send_mail

from readthedocs.worker import app

log = logging.getLogger(__name__)

PRODUCTION_DOMAIN = getattr(settings, 'PRODUCTION_DOMAIN')
DOCS_ITALIA_CONVERSION_UPLOAD_PATH = os.path.join(settings.MEDIA_URL, 'tmp')
DOCS_ITALIA_CONVERTER_EMAIL = getattr(settings, 'DOCS_ITALIA_CONVERTER_EMAIL', 'info@example.org')


@app.task(queue='web')
def process_file(email, saved, unique_key):
    """
    This celery task save the uploaded file from memory to the
    tmp folder and calls the `converti` command on it.
    Than emails the user with the link to download the converted file.
    :param email: the user email
    :param saved: The full path of the uploaded file
    :parma unique_key: the unique name of the new folder
    """
    file_path, file_name = os.path.split(saved)
    new_file_name = os.path.splitext(os.path.basename(file_name))[0] + '.rst'
    with open(os.path.join(file_path, new_file_name), 'w') as out:
        subprocess.call(['pandoc', saved], stdout=out)
    log.info('Processing uploaded file {} from {}'.format(saved, email))
    send_mail(
        'Conversione del documento effettuata',
        'http://{}{}/{}/{}'.format(
            PRODUCTION_DOMAIN, DOCS_ITALIA_CONVERSION_UPLOAD_PATH,
            unique_key,
            new_file_name
        ),
        DOCS_ITALIA_CONVERTER_EMAIL,
        [email],
        fail_silently=False,
    )
