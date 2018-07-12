# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import os
from tempfile import mkstemp
from unittest.mock import patch

from django.core import mail
from django.test import TestCase
from docs_italia_convertitore_web.tasks import process_file


class TaskTest(TestCase):

    @patch('docs_italia_convertitore_web.tasks._run_pandoc')
    @patch('docs_italia_convertitore_web.tasks.make_archive')
    @patch('docs_italia_convertitore_web.tasks.sentry_message')
    def test_pandoc_error(self, sentry_message, make_archive, _run_pandoc):
        error_msg = 'errored'
        _run_pandoc.return_value = (
            None, error_msg
        )
        make_archive.return_value = True
        sentry_message.return_value = True
        process_file.apply(('test@email.com', '/tmp/some file.doc', 'super_unique', False), )
        self.assertEqual(sentry_message.call_count, 1)
        self.assertEqual(
            sentry_message.call_args[1]['extra']['original_file_url'],
            'http://convert.com/media/tmp/super_unique/some%20file.zip'
        )
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Errore conversione documento di DOCS ITALIA')
        self.assertEqual(message.body, error_msg)

    @patch('docs_italia_convertitore_web.tasks._run_pandoc')
    @patch('docs_italia_convertitore_web.tasks.make_archive')
    @patch('docs_italia_convertitore_web.tasks.sentry_message')
    def test_pandoc_run(self, sentry_message, make_archive, _run_pandoc):
        _run_pandoc.return_value = (
            None, None
        )
        make_archive.return_value = True
        sentry_message.return_value = True
        process_file.apply(('test@email.com', '/tmp/some file.doc', 'super_unique', False), )
        sentry_message.assert_not_called()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Conversione documento di DOCS ITALIA')
        self.assertEqual(message.body, 'http://convert.com/media/tmp/super_unique/some%20file.rst')

    @patch('docs_italia_convertitore_web.tasks._run_converti')
    @patch('docs_italia_convertitore_web.tasks.make_archive')
    @patch('docs_italia_convertitore_web.tasks.sentry_message')
    def test_converti_error(self, sentry_message, make_archive, _run_converti):
        error_msg = 'errored'
        _run_converti.return_value = (
            None, error_msg
        )
        make_archive.return_value = True
        sentry_message.return_value = True
        process_file.apply(('test@email.com', '/tmp/some file.docx', 'super_unique'), )
        self.assertEqual(sentry_message.call_count, 1)
        self.assertEqual(
            sentry_message.call_args[1]['extra']['original_file_url'],
            'http://convert.com/media/tmp/super_unique/some%20file.zip'
        )
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Errore conversione documento di DOCS ITALIA')
        self.assertEqual(message.body, error_msg)

    @patch('docs_italia_convertitore_web.tasks._run_converti')
    @patch('docs_italia_convertitore_web.tasks.make_archive')
    @patch('docs_italia_convertitore_web.tasks.sentry_message')
    def test_converti_run(self, sentry_message, make_archive, _run_converti):
        fp, path = mkstemp(suffix='.docx')
        _run_converti.return_value = (
            None, None
        )
        make_archive.return_value = True
        sentry_message.return_value = True
        os.makedirs(os.path.join(os.path.dirname(path), 'risultato-conversione'), exist_ok=True)
        process_file.apply(('test@email.com', path, 'super_unique'), )
        sentry_message.assert_not_called()
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        new_file = os.path.splitext(os.path.basename(path))[0]
        self.assertEqual(message.subject, 'Conversione documento di DOCS ITALIA')
        self.assertEqual(message.body, 'http://convert.com/media/tmp/super_unique/%s.zip' % new_file)
