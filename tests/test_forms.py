# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import json
import os
import shutil
from tempfile import mkdtemp

from django.test import TestCase
from docs_italia_convertitore_web.forms import ItaliaConverterForm


class TaskTest(TestCase):

    def test_options(self):
        path = mkdtemp()
        data = {
            'email': 'test@example.com',
            'normattiva': True,
            'celle_complesse': False,
            'preserva_citazioni': True,
            'dividi_sezioni': False
        }
        expected = {
            'collegamento-normattiva': True,
            'celle-complesse': False,
            'preserva-citazioni': True,
            'dividi-sezioni': False
        }
        form = ItaliaConverterForm(data)
        self.assertTrue(form.is_valid())
        json_file = form.get_options_json(path)
        self.assertTrue(os.path.exists(json_file))
        with open(json_file, 'r') as fp:
            option = json.load(fp)
        self.assertDictEqual(option, expected)
        shutil.rmtree(path)
