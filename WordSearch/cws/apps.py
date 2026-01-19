from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class CwsConfig(AppConfig):
    name = 'cws'
    verbose_name = 'Find Your Words'

class MyAdminConfig(AdminConfig):
    default_site = 'cws.admin.MyAdminSite'


