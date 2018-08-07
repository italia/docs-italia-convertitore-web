# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase

from docs_italia_convertitore_web.views import FileUploadView

User = get_user_model()


class ViewsTest(TestCase):

    def test_no_initial(self):
        response = self.client.get(reverse('docs_italia_convertitore_web:docs-italia-converter-view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<input class="form-control" data-msg="Email non valida" id="id_email" name="email" type="email" />'
        )

    def test_initial(self):
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='test')

        request = RequestFactory().get(reverse('docs_italia_convertitore_web:docs-italia-converter-view'))
        request.user = user
        view = FileUploadView()
        view.request = request
        response = view.get(request)
        self.assertEqual(response.status_code, 200)
        response.render()
        self.assertContains(response, 'value="testuser@example.com"')
