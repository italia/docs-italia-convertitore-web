# -*- coding: utf-8 -*-
"""Public project views."""
from __future__ import absolute_import
from __future__ import unicode_literals

from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from .forms import ItaliaConverterForm
from .tasks import process_file


class FileUploadView(FormView):

    """File Upload view"""

    template_name = 'docs_italia_convertitore_web/converter_index.html'
    form_class = ItaliaConverterForm

    def form_valid(self, form):
        """ the form valid function, calls the celery process task """
        uploaded = form.cleaned_data['file']
        email = form.cleaned_data['email']
        process_file.delay(email, uploaded)
        return super(FileUploadView, self).form_valid(form)

    def form_invalid(self, form):
        response = super(FileUploadView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def get_success_url(self):
        return reverse('docs_italia_convertitore:conversion-started')
