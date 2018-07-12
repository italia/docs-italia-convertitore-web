# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from .views import FileUploadView

app_name = 'docs_italia_convertitore_web'
urlpatterns = [
    url(r'^$', FileUploadView.as_view(), name='docs-italia-converter-view'),
    url(r'message$',
        TemplateView.as_view(template_name='docs_italia_convertitore_web/converter_started.html'),
        name='conversion-started'
        ),
]
