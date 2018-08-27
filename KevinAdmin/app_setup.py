from django.conf import settings


def kevinadmin_auto_discover():
    for app_name in settings.INSTALLED_APPS:
        try:
            mod = __import__('%s.kevinadmin' % app_name)
        except Exception as e:
            pass
