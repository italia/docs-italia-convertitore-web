# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.conf.urls import include, url

urlpatterns = [
    url(r'converti/', include('docs_italia_convertitore_web.urls', namespace='docs_italia_convertitore'))
]
