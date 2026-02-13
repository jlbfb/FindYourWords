"""
WSGI config for WordSearch project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import environ

env = environ.Env()
environ.Env.read_env()


from django.core.wsgi import get_wsgi_application

os.environ.setdefault(env("DJANGO_SETTINGS_MODULE"), "WordSearch.settings_prod")

application = get_wsgi_application()
