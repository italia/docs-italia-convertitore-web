=====
Usage
=====

Per utilizzare l'applicazione aggiungere docs_italia_convertitore_web alle `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        # docsitalia
        'readthedocs.docsitalia',
        'docs_italia_convertitore_web',
        ...
    )

Aggiungere le url nel file readthedocs/docsitalia/urls.py

.. code-block:: python

docsitalia_urls.insert(0, url(r'', include('docs_italia_convertitore.urls', namespace='docs_italia_convertitore')))

