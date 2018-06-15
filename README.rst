=============================
docs-italia-convertitore
=============================

Applicazione Django che si interfaccia con :
`docs-italia-convertitore <https://github.com/italia/docs-italia-comandi-conversione>`_

Quickstart
----------

Prima di tutto è necessario seguire l'installazione di questi due pacchetti:

https://github.com/italia/docs-italia-comandi-conversione#installazione
e
https://github.com/italia/docs-italia-pandoc-filters#installazione

Assicurarsi inoltre che il comando converti sia eseguibile dalla propria shell, se 
questo non avenisse è necessario aggiungere al proprio .bashrc quest riga:
export PATH=$HOME/.local/bin:$PATH
e ricaricare il proprio bashrc . ~/.bashrc

Fatto questo installa il pacchetto con:

    pip install git+https://github.com/italia/docs-italia-convertitore-web.git

aggiungi alle `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'docs_italia_convertitore_web',
        ...
    )

E per finire includi le urls del pacchetto nel file: readthedocs/docsitalia/urls.py

.. code-block:: python

    docsitalia_urls.insert(0, url(r'', include('docs_italia_convertitore_web.urls', namespace='docs_italia_convertitore')))

