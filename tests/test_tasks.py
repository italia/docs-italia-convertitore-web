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
    def test_pandoc_error(self, patched):
        error_msg = 'errored'
        patched.return_value = (
            None, error_msg
        )
        process_file.apply(('test@email.com', 'some file.doc', 'super_unique'), )
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Errore conversione documento di DOCS ITALIA')
        self.assertEqual(message.body, error_msg)

    @patch('docs_italia_convertitore_web.tasks._run_pandoc')
    def test_pandoc_run(self, patched):
        patched.return_value = (
            None, None
        )
        process_file.apply(('test@email.com', 'some file.doc', 'super_unique'), )
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Conversione documento di DOCS ITALIA')
        self.assertEqual(message.body, 'http://convert.com/media/tmp/super_unique/some+file.rst')

    @patch('docs_italia_convertitore_web.tasks._run_converti')
    def test_converti_error(self, patched):
        error_msg = 'errored'
        patched.return_value = (
            None, error_msg
        )
        process_file.apply(('test@email.com', 'some file.docx', 'super_unique'), )
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'Errore conversione documento di DOCS ITALIA')
        self.assertEqual(message.body, error_msg)

    @patch('docs_italia_convertitore_web.tasks._run_converti')
    @patch('docs_italia_convertitore_web.tasks.make_archive')
    def test_converti_run(self, make_archive, _run_converti):
        fp, path = mkstemp(suffix='.docx')
        _run_converti.return_value = (
            None, None
        )
        make_archive.return_value = True
        os.makedirs(os.path.join(os.path.dirname(path), 'risultato-conversione'), exist_ok=True)
        process_file.apply(('test@email.com', path, 'super_unique'), )
        self.assertEqual(len(mail.outbox), 1)
        message = mail.outbox[0]
        new_file = os.path.splitext(os.path.basename(path))[0]
        self.assertEqual(message.subject, 'Conversione documento di DOCS ITALIA')
        self.assertEqual(message.body, 'http://convert.com/media/tmp/super_unique/%s.zip' % new_file)
