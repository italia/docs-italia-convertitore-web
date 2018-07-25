# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json
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
        self.assertIn(error_msg, message.body)
        self.assertIn('Conversion ID', message.body)

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
        self.assertIn('http://convert.com/media/tmp/super_unique/some%20file.rst', message.body)
        self.assertIn('Conversion ID', message.body)

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
        self.assertIn(error_msg, message.body)
        self.assertIn('Conversion ID', message.body)

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
        self.assertIn('http://convert.com/media/tmp/super_unique/%s.zip' % new_file, message.body)
        self.assertIn('Conversion ID', message.body)

    @patch('docs_italia_convertitore_web.tasks.subprocess.check_output')
    @patch('docs_italia_convertitore_web.tasks.make_archive')
    @patch('docs_italia_convertitore_web.tasks.sentry_message')
    def test_converti_json(self, sentry_message, make_archive, check_output):
        fp, path = mkstemp(suffix='.docx')
        check_output.return_value = True
        make_archive.return_value = True
        sentry_message.return_value = True

        base_dir = os.path.dirname(path)
        os.makedirs(os.path.join(base_dir, 'risultato-conversione'), exist_ok=True)
        json_options = os.path.join(base_dir, 'options.json')
        options = {
            'normattiva': True,
            'celle-complesse': False,
            'preserva-citazioni': True,
            'dividi-sezioni': False
        }
        with open(json_options, 'w') as fp:
            json.dump(options, fp)

        process_file.apply(('test@email.com', path, 'super_unique', True, json_options), )
        sentry_message.assert_not_called()
        self.assertEqual(check_output.call_count, 1)
        args = ['converti', path, '--opzioni-json', json_options]
        self.assertEqual(args, list(check_output.call_args)[0][0])
