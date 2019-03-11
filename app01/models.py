from django.db import models


class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(max_length=32, verbose_name='部门名称')


class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.CharField(verbose_name='年龄', max_length=32)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    depart = models.ForeignKey(verbose_name='部门', to='Department', on_delete=models.CASCADE)
