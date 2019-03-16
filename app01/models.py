from django.db import models


class Department(models.Model):
    """
    部门表
    """
    title = models.CharField(max_length=32, verbose_name='部门名称')

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    """
    MALE = 1
    FEMALE = 2
    GENDER_ITEMS = (
        (MALE, '男'),
        (FEMALE, '女')
    )
    CLASSES_ITEMS = (
        (11, 'python'),
        (22, 'go'),
        (33, 'javascript'),
        (44, 'java')
    )

    name = models.CharField(verbose_name='姓名', max_length=32)
    gender = models.IntegerField(verbose_name='性别', choices=GENDER_ITEMS, default=1)
    classes = models.IntegerField(verbose_name='班级', choices=CLASSES_ITEMS, default=11)

    age = models.CharField(verbose_name='年龄', max_length=32)
    email = models.CharField(verbose_name='邮箱', max_length=32)
    depart = models.ForeignKey(verbose_name='部门', to='Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Deploy(models.Model):
    STATUS_ITEMS = (
        (1, '在线'),
        (2, '离线'),
    )
    title = models.CharField(verbose_name='标题', max_length=32)
    status = models.PositiveIntegerField(verbose_name='状态', choices=STATUS_ITEMS, default=1)

    def __str__(self):
        return self.title
