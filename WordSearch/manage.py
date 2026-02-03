#!/usr/bin/env python
import environ
from pathlib import Path
import sys


env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = BASE_DIR / 'WordSearch' / '.env'
environ.Env.read_env(ENV_FILE_PATH)

if __name__ == "__main__":
    DJANGO_SETTINGS_MODULE = env('DJANGO_SETTINGS_MODULE')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
