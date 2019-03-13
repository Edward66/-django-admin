from django.shortcuts import HttpResponse

from app02 import models
from stark.service.version1 import site
from stark.service.version1 import StarkHandler


class HostHandler(StarkHandler):
    pass


class RoleHandler(StarkHandler):
    pass


class ProjectHandler(StarkHandler):
    pass


site.register(models.Host)
site.register(models.Role)
site.register(models.Project)
