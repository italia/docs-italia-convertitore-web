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
from django.template.loader import render_to_string
from django.utils.encoding import force_text
from django.utils.http import urlquote

from .utils import sentry_message

log = logging.getLogger(__name__)

PRODUCTION_DOMAIN = getattr(settings, 'PRODUCTION_DOMAIN')
DOCS_ITALIA_CONVERSION_UPLOAD_PATH = os.path.join(settings.MEDIA_URL, 'tmp')
DOCS_ITALIA_CONVERTER_EMAIL = getattr(settings, 'DOCS_ITALIA_CONVERTER_EMAIL', 'info@example.org')


def _run_converti(uploaded_file, new_file_name, file_path, options_json=None):
    """
    Run converti and report output messages

    :param uploaded_file: uploaded file
    :param new_file_name: converted file name
    :param file_path: source path

    :return: error messages
    """
    err_msg = None
    out_msg = None
    options = []
    if options_json:
        options = ['--opzioni-json', options_json]
    try:
        out_msg = subprocess.check_output(
            ['converti', uploaded_file] + options, stderr=subprocess.STDOUT, cwd=file_path
        )
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
    :param options_json: optional path to the `converti` command options json file

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
def process_file(email, uploaded_file, unique_key, use_converti=True, options_json=None):
    """
    This celery task save the uploaded file from memory to the
    tmp folder and calls the ``pandoc`` or ``converti`` command on it.
    Than emails the user with the link to download the converted file or the error message

    :param email: the user email
    :param uploaded_file: the full path of the uploaded file
    :param unique_key: the unique name of the new folder
    :param use_converti: run ``converti`` command (true) or ``pandoc`` (false). As of now we always run converti
    :param options_json: optional path to the `converti` command options json file
    """
    file_path, file_name = os.path.split(uploaded_file)
    new_file_name = '%s.rst' % os.path.splitext(os.path.basename(file_name))[0]
    log.info('Processing uploaded file {} from {}'.format(uploaded_file, email))
    if use_converti:
        out_msg, err_msg = _run_converti(uploaded_file, new_file_name, file_path, options_json)
        if not err_msg:
            new_file_name = os.path.splitext(os.path.basename(file_name))[0]
            os.chdir(os.path.join(file_path, 'risultato-conversione'))
            make_archive(os.path.join(file_path, new_file_name), 'zip', '.')
            new_file_name = '%s.zip' % new_file_name
    else:
        out_msg, err_msg = _run_pandoc(uploaded_file, new_file_name, file_path)
    if err_msg:
        # zipping the content of the folder for inspection
        # reporting the URL to download the document through sentry
        os.chdir(file_path)
        error_package = os.path.splitext(os.path.basename(file_name))[0]
        make_archive(os.path.join(file_path, error_package), 'zip', '.')
        original_path = os.path.join(
            DOCS_ITALIA_CONVERSION_UPLOAD_PATH,
            unique_key,
            urlquote('%s.zip' % error_package)
        )
        context = {
            'file_name': file_name,
            'path': original_path,
            'conversion_id': unique_key,
            'output_message': '%s %s' % (out_msg, err_msg)
        }
        template = 'docs_italia_convertitore_web/email/error_body.html'
        subject = 'Errore conversione documento di DOCS ITALIA'
        sentry_message('There was an error processing %s: %s %s' % (uploaded_file, out_msg, err_msg), extra={
            'original_file_url': original_path
        })
    else:
        path = os.path.join(
            DOCS_ITALIA_CONVERSION_UPLOAD_PATH,
            unique_key,
            urlquote(new_file_name)
        )
        context = {
            'path': path,
            'conversion_id': unique_key
        }
        template = 'docs_italia_convertitore_web/email/success_body.html'
        subject = 'Conversione documento di DOCS ITALIA'
    body = render_to_string(template, context=context)
    send_mail(
        subject,
        body,
        DOCS_ITALIA_CONVERTER_EMAIL,
        [email],
        fail_silently=False,
    )
