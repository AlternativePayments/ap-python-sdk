== README

== PREREQUISITE

    - Installed python 2.7+
    - Installed pip
    - Installed django
    - Installed django-markdown-deux
    - Installed ap_python_sdk (using pip is one of the ways...)

== RUNNING APPLICATION

     Python 2.x:

        - Clone repo
        - Inside folder +sample_application/sample_application/ap_python_sdk_key.py+ set your account key
            eg. +ap_python_sdk.api_key = 'Test/Live key provided in your Alternative Payments account'+
        - Start Django server by runing +python manage.py runserver+ from inside folder +sample+
        - If your setup is default one then access application on +http://localhost:8000/app+

    Pyton 3.x:
        - Clone repo
        - Inside folder +sample_application/sample_application/ap_python_sdk_key.py+ set your account key
        - Because of https://www.python.org/dev/peps/pep-0404/, you will need to change imports as follows:
            - app/urls.py: from `import views` to `from  app import views`
            - app/views/__init__.py: for all imports following example: from `from customers import *` to `from .customers import *`
            - sample_application/settings.py: from `import ap_python_sdk_key` to `from .ap_python_sdk_key import *`
        - Start Django server by runing +python manage.py runserver+ from inside folder +sample+
        - If your setup is default one then access application on +http://localhost:8000/app+