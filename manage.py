#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import nltk
from pathlib import Path

# nltk_data_path = "C:\\Users\\admin\\AppData\\Roaming\\nltk_data"  # <--- VERY IMPORTANT: Double check this path

nltk_data_path = 'nltk_data'
nltk.data.path.append(nltk_data_path)
# Set nltk data path


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Diary.settings')
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


