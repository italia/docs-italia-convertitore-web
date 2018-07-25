# -*- coding: utf-8 -*-
"""Public project views."""
from __future__ import absolute_import, unicode_literals

import json
import os

from django import forms
from django.utils.translation import ugettext_lazy as _


class ItaliaConverterForm(forms.Form):
    """ Italia converter Form """
    email = forms.EmailField(label=_('email'), required=True)
    file = forms.FileField(label=_('file'), required=False)
    normattiva = forms.BooleanField(
        label=_('Collegamenti normattiva'), required=False,
        help_text=_('<a target="blank" href="https://github.com/italia/docs-italia-comandi-conversione/blob/'
                    'master/doc/comandi/converti-opzioni.md#collegamento-normattiva">Informazioni di dettaglio</a>')
    )
    celle_complesse = forms.BooleanField(
        label=_('Celle complesse'), required=False,
        help_text=_('<a target="blank" href="https://github.com/italia/docs-italia-comandi-conversione/blob/'
                    'master/doc/comandi/converti-opzioni.md#celle-complesse">Informazioni di dettaglio</a>')
    )
    preserva_citazioni = forms.BooleanField(
        label=_('Preserva citazioni'), required=False,
        help_text=_('<a target="blank" href="https://github.com/italia/docs-italia-comandi-conversione/blob/'
                    'master/doc/comandi/converti-opzioni.md#preserva-citazioni">Informazioni di dettaglio</a>')
    )
    dividi_sezioni = forms.BooleanField(
        label=_('Dividi sezioni'), required=False,
        help_text=_('<a target="blank" href="https://github.com/italia/docs-italia-comandi-conversione/blob/'
                    'master/doc/comandi/converti-opzioni.md#dividi-sezioni">Informazioni di dettaglio</a>')
    )

    converter_options = ['normattiva', 'celle_complesse', 'preserva_citazioni', 'dividi_sezioni']

    def get_options_json(self, folder):
        """ Saves the converter options as json file suitable for `converti` command """
        options = {
            # Rif italia/docs-italia-comandi-conversione/doc/comandi/converti-opzioni.md#dividi-sezioni
            'dividi-sezioni': self.cleaned_data['dividi_sezioni'],
            # Rif italia/docs-italia-comandi-conversione/doc/comandi/converti-opzioni.md#collegamento-normattiva
            'collegamento-normattiva': self.cleaned_data['normattiva'],
            # Rif italia/docs-italia-comandi-conversione/doc/comandi/converti-opzioni.md#celle-complesse
            'celle-complesse': self.cleaned_data['celle_complesse'],
            # Rif italia/docs-italia-comandi-conversione/doc/comandi/converti-opzioni.md#preserva-citazioni
            'preserva-citazioni': self.cleaned_data['preserva_citazioni'],
        }
        with open(os.path.join(folder, 'options.json'), 'w') as fp:
            json.dump(options, fp)
        return os.path.join(folder, 'options.json')
