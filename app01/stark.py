from django.urls import re_path
from django.shortcuts import HttpResponse

from stark.service.version1 import site
from stark.service.version1 import StarkHandler

from app01 import models


class DeaprtmentHandler(StarkHandler):
    list_display = ['id', 'title']


class UserInfoHandler(StarkHandler):
    # 定制页面显示的列
    list_display = ['name', 'age', 'email']

    def get_list_display(self):
        """

        :return:
        """
        return ['name', 'age']


site.register(models.Department, DeaprtmentHandler)

site.register(models.UserInfo, UserInfoHandler)
