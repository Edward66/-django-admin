from django.shortcuts import HttpResponse
from stark.service.version1 import site

from app02 import models


class HostHandler:
    def __init__(self, model_class):
        self.model_class = model_class

    def list_view(self, request):
        """
        列表页面
        :param request:
        :return:
        """
        return HttpResponse('主机列表页面')

    def add_view(self, request):
        """
        添加页面
        :param request:
        :return:
        """

    def edit_view(self, request, pk):
        """
        编辑页面
        :param request:
        :param pk:
        :return:
        """

    def delete_view(self, request, pk):
        """
        删除页面
        :param request:
        :param pk:
        :return:
        """


class RoleHandler:
    def __init__(self, model_class):
        self.model_class = model_class

    def list_view(self, request):
        """
        列表页面
        :param request:
        :return:
        """
        return HttpResponse('角色列表页面')

    def add_view(self, request):
        """
        添加页面
        :param request:
        :return:
        """

    def edit_view(self, request, pk):
        """
        编辑页面
        :param request:
        :param pk:
        :return:
        """

    def delete_view(self, request, pk):
        """
        删除页面
        :param request:
        :param pk:
        :return:
        """


site.register(models.Host, HostHandler)
site.register(models.Role, RoleHandler)
