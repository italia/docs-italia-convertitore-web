# -*- coding: utf-8 -*-
"""Public project views."""
from __future__ import absolute_import, unicode_literals

import json
import os

from django import forms
from django.utils.translation import ugettext_lazy as _


class ItaliaConverterForm(forms.Form):
    """ Italia converter Form """
    email = forms.EmailField(label=_('email'), required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'data-msg': 'Email non valida'}))
    file = forms.FileField(label=_('file'), required=False)
    normattiva = forms.BooleanField(
        label=_('Collegamenti normattiva'), required=False,
        help_text=_('<p>Con questa opzione abilitata, vengono trasformati tutti i riferimenti a leggi e normative in collegamenti ipertestuali al sito di Normattiva.</p><p><a target="blank" href="https://github.com/italia/docs-italia-comandi-conversione/blob/'
                    'master/doc/comandi/converti-opzioni.md#collegamento-normattiva" class="d-block text-uppercase font-weight-bold x-small">Vai alla linea guida →</a></p>')
    )
    celle_complesse = forms.BooleanField(
        label=_('Celle complesse'), required=False,
        help_text=_('<p>Con questa opzione abilitata, il processo di conversione evita di mandare a capo il contenuto delle celle mantenendolo tutto sulla stessa riga.</p><p><a target="blank" href="https://github.com/italia/docs-italia-comandi-conversione/blob/'
                    'master/doc/comandi/converti-opzioni.md#celle-complesse" class="d-block text-uppercase font-weight-bold x-small">Vai alla linea guida →</a></p>')
    )
    preserva_citazioni = forms.BooleanField(
        label=_('Preserva citazioni'), required=False,
        help_text=_('<p>Con questa opzione abilitata, il testo indentato viene interpretato come citazione.</p><p><a target="blank" href="https://github.com/italia/docs-italia-comandi-conversione/blob/'
                    'master/doc/comandi/converti-opzioni.md#preserva-citazioni" class="d-block text-uppercase font-weight-bold x-small">Vai alla linea guida →</a></p>')
    )
    dividi_sezioni = forms.BooleanField(
        label=_('Dividi sezioni'), required=False,
        help_text=_('<p>Con questa opzione abilitata, la struttura dei files viene divisa solo in base alle sezioni di primo livello.</p><p><a target="blank" href="https://github.com/italia/docs-italia-comandi-conversione/blob/'
                    'master/doc/comandi/converti-opzioni.md#dividi-sezioni" class="d-block text-uppercase font-weight-bold x-small">Vai alla linea guida →</a></p>')
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
