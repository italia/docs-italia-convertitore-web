=============================
docs-italia-convertitore
=============================

Applicazione Django che si interfaccia con il convertitore pandoc


Quickstart
----------

Install docs-italia-convertitore::

    pip install git+https://github.com/italia/docs-italia-convertitore-web.git

Aggiungi alle `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'docs_italia_convertitore_web',
        ...
    )

Add docs-italia-convertitore's URL patterns:

.. code-block:: python

    from docs_italia_convertitore import urls as docs_italia_convertitore_urls


    urlpatterns = [
        ...
        url(r'^', include(docs_italia_convertitore_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
