from django.urls import re_path
from django.utils.safestring import mark_safe  # 让字符串可以作为html标签显示在页面
from django.shortcuts import HttpResponse

from stark.service.version1 import site
from stark.service.version1 import StarkHandler

from app01 import models


class DeaprtmentHandler(StarkHandler):
    list_display = ['id', 'title']


class UserInfoHandler(StarkHandler):
    def display_edit(self, obj=None, is_header=None):
        """
        自定义页面显示的列（表头和内容）
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '编辑表头'

        return mark_safe('<a href="https://www.baidu.com">编辑</a>')

    def display_del(self, obj=None, is_header=None):
        if is_header:
            return '删除表头'
        return mark_safe('<a href="https://www.baidu.com">删除</a>')

    # 定制页面显示的列
    # 前面没有对象，相当于写了 UserInfoHandler.display_edit
    list_display = ['name', 'age', 'email', display_edit, display_del]


site.register(models.Department, DeaprtmentHandler)

site.register(models.UserInfo, UserInfoHandler)
