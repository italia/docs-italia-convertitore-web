# -*- coding: utf-8 -*-
"""Public project views."""
from __future__ import absolute_import, unicode_literals

from django import forms


class ItaliaConverterForm(forms.Form):
    """ Italia converter Form """
    email = forms.EmailField()
    file = forms.FileField()
    monospace = forms.BooleanField(required=False)
