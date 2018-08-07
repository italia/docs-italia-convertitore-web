# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals


def sentry_message(message, **kwargs):
    """
    Log a message to sentry, including the stack trace and extra variables

    Log level can be set by adding a ``log_level`` key to :data:`kwargs`.
    Default is ``info``

    Example:

    .. code-block::python

       sentry_message('IMPORT: file received', extra={
           'args': kwargs, 'path': path, 'zipped': self.zipped
       })

    :param message: message text
    :type message: string
    :param kwargs: context to be logged
    :type kwargs: dict
    :return: None
    """
    from raven.contrib.django.models import client
    kwargs['stack'] = True
    kwargs['data'] = {'level': kwargs.get('log_level', 'info')}
    client.captureMessage(message, **kwargs)
