import sys
import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "堡垒机.settings")
    import django

    django.setup()
    from backend import main

    interactive_obj = main.ArgvHandler(sys.argv)
    interactive_obj.call()