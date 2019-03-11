from django.shortcuts import HttpResponse
from stark.service.version1 import site

from app01 import models


class DeaprtmentHandler:
    def __init__(self, model_class):
        self.model_class = model_class

    def list_view(self, request):
        """
        列表页面
        :param request:
        :return:
        """
        return HttpResponse('部门列表页面')

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


class UserInfoHandler:
    def __init__(self, model_class):
        self.model_class = model_class

    def list_view(self, request):
        """
        列表页面
        :param request:
        :return:
        """
        return HttpResponse('用户列表页面')

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


site.register(models.Department, DeaprtmentHandler)
site.register(models.UserInfo, UserInfoHandler)
