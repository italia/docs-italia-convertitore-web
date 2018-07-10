# -*- coding: utf-8 -*-
"""Public project views."""
from __future__ import absolute_import, unicode_literals

import logging
import os
import subprocess
from shutil import make_archive

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_text
from django.utils.http import urlquote

log = logging.getLogger(__name__)

PRODUCTION_DOMAIN = getattr(settings, 'PRODUCTION_DOMAIN')
DOCS_ITALIA_CONVERSION_UPLOAD_PATH = os.path.join(settings.MEDIA_URL, 'tmp')
DOCS_ITALIA_CONVERTER_EMAIL = getattr(settings, 'DOCS_ITALIA_CONVERTER_EMAIL', 'info@example.org')


def _run_converti(uploaded_file, new_file_name, file_path):
    """
    Run converti and report output messages

    :param uploaded_file: uploaded file
    :param new_file_name: converted file name
    :param file_path: source path

    :return: error messages
    """
    err_msg = None
    out_msg = None
    try:
        out_msg = subprocess.check_output(['converti', uploaded_file], stderr=subprocess.STDOUT, cwd=file_path)
    except subprocess.CalledProcessError as e:
        err_msg = e.output
    except Exception as e:
        err_msg = '%s - %s' % (out_msg, force_text(e))
    return out_msg, err_msg


def _run_pandoc(uploaded_file, new_file_name, file_path):
    """
    Run pandoc and report output messages

    :param uploaded_file: uploaded file
    :param new_file_name: converted file name
    :param file_path: source path

    :return: error messages
    """
    err_msg = None
    out_msg = None
    args = ['pandoc', uploaded_file, '-o', os.path.join(file_path, new_file_name)]
    try:
        out_msg = subprocess.check_output(args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        err_msg = '%s - %s' % (out_msg, force_text(e.output))
    except Exception as e:
        err_msg = '%s - %s' % (out_msg, force_text(e))
    return out_msg, err_msg


@shared_task(queue='web')
def process_file(email, uploaded_file, unique_key):
    """
    This celery task save the uploaded file from memory to the
    tmp folder and calls the ``pandoc`` or ``converti`` command on it.
    Than emails the user with the link to download the converted file or the error message

    TODO: Report back to the frontend the conversion status

    :param email: the user email
    :param uploaded_file: the full path of the uploaded file
    :param unique_key: the unique name of the new folder
    """
    file_path, file_name = os.path.split(uploaded_file)
    new_file_name = '%s.rst' % os.path.splitext(os.path.basename(file_name))[0]
    log.info('Processing uploaded file {} from {}'.format(uploaded_file, email))
    if os.path.splitext(file_name)[1].lower() == '.docx':
        out_msg, err_msg = _run_converti(uploaded_file, new_file_name, file_path)
        if not err_msg:
            new_file_name = os.path.splitext(os.path.basename(file_name))[0]
            os.chdir(os.path.join(file_path, 'risultato-conversione'))
            make_archive(os.path.join(file_path, new_file_name), 'zip', '.')
            new_file_name = '%s.zip' % new_file_name
    else:
        out_msg, err_msg = _run_pandoc(uploaded_file, new_file_name, file_path)
    if err_msg:
        log.error('There was an error processing %s: %s %s' % (uploaded_file, out_msg, err_msg))
        send_mail(
            'Errore conversione documento di DOCS ITALIA',
            err_msg,
            DOCS_ITALIA_CONVERTER_EMAIL,
            [email],
            fail_silently=False,
        )
    else:
        msg = '{}/{}/{}'.format(
            DOCS_ITALIA_CONVERSION_UPLOAD_PATH,
            unique_key,
            urlquote(new_file_name)
        )
        send_mail(
            'Conversione documento di DOCS ITALIA',
            msg,
            DOCS_ITALIA_CONVERTER_EMAIL,
            [email],
            fail_silently=False,
        )
