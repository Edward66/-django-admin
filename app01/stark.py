from django.urls import re_path
from django.shortcuts import HttpResponse

from stark.service.version1 import site
from stark.service.version1 import StarkHandler

from app01 import models


class DeaprtmentHandler(StarkHandler):

    def extra_urls(self):
        """
        额外的增加URL
        :return:
        """
        return [
            re_path(r'^detail/(\d+)/$', self.detail_view)
        ]

    def detail_view(self, request, pk):
        return HttpResponse('详细页面')


class UserInfoHandler(StarkHandler):

    def get_urls(self):
        """
        修改所有的URL
        :return:
        """
        patterns = [
            re_path(r'^list/$', self.list_view),
            re_path(r'^add/$', self.add_view),
        ]
        return patterns


site.register(models.Department, DeaprtmentHandler)

site.register(models.UserInfo, UserInfoHandler, 'private')
