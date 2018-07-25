# -*- coding: utf-8 -*-
"""Public project views."""
from __future__ import absolute_import, unicode_literals

import os
import uuid

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic.edit import FormView

from .forms import ItaliaConverterForm
from .tasks import process_file

CONVERSION_UPLOAD_DIR = os.path.join(settings.MEDIA_ROOT, 'tmp')


class FileUploadView(FormView):

    """File Upload view"""

    template_name = 'docs_italia_convertitore_web/converter_index.html'
    form_class = ItaliaConverterForm

    def form_valid(self, form):
        """
        the form valid function save the file from memory to a
        unique folder than calls the celery process task
        """
        uploaded = form.cleaned_data['file']
        email = form.cleaned_data['email']
        unique_key = uuid.uuid1().hex
        new_folder_name = os.path.join(CONVERSION_UPLOAD_DIR, unique_key)
        os.makedirs(new_folder_name, exist_ok=True)
        saved = os.path.join(CONVERSION_UPLOAD_DIR, new_folder_name, uploaded.name)
        with default_storage.open(saved, 'wb+') as destination:
            for chunk in uploaded.chunks():
                destination.write(chunk)
        options_json = form.get_options_json(new_folder_name)
        process_file.delay(email, saved, unique_key, options_json=options_json)
        return super(FileUploadView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(FileUploadView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return response

    def get_success_url(self):
        return reverse('docs_italia_convertitore:conversion-started')
