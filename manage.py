#!/usr/bin/env python
"""Django entry point so you can run manage.py from the repo root."""
import os
import sys
from pathlib import Path


def main():
    backend = Path(__file__).resolve().parent / 'backend'
    os.chdir(backend)
    sys.path.insert(0, str(backend))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'camp.settings')
    if 'runserver' in sys.argv:
        from camp.frontend_dev import configure_runserver_port, ensure_frontend

        configure_runserver_port(sys.argv)
        ensure_frontend()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
