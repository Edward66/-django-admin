from django.shortcuts import HttpResponse

from app02 import models
from stark.service.version1 import site
from stark.service.version1 import StarkHandler


class HostHandler(StarkHandler):
    list_display = ['id', 'host', 'ip']


class RoleHandler(StarkHandler):
    pass


class ProjectHandler(StarkHandler):
    pass


site.register(models.Host, HostHandler)
site.register(models.Role)

site.register(models.Project)
site.register(models.Project, prev='private')
