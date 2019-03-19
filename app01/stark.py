from django.shortcuts import redirect

from stark.service.version1 import site
from stark.service.version1 import StarkHandler, get_choice_text, StarkModelForm, Option

from app01 import models


class MyOption(Option):
    def get_db_condition(self, request, *args, **kwargs):
        return {}
        # return {'id__gt': request.GET.get('nid')}


class UserInfoModelForm(StarkModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'gender', 'classes', 'age', 'email']


class DeaprtmentHandler(StarkHandler):
    has_add_btn = True
    search_list = ['title']
    list_display = ['id', 'title', StarkHandler.display_edit, StarkHandler.display_del]


class UserInfoHandler(StarkHandler):
    # depart：foreign_key用__str__显示（在models里定义）
    list_display = [
        StarkHandler.display_checkbox,
        'name',
        get_choice_text('性别', 'gender'),
        get_choice_text('班级', 'classes'),
        'age',
        'email',
        'depart',
        StarkHandler.display_edit,
        StarkHandler.display_del
    ]

    per_page_count = 10

    has_add_btn = True

    # model_form_class = UserInfoModelForm

    order_list = ['id']

    # # 姓名中含有关键字或邮箱中含有关键字
    search_list = ['name__contains', 'email__contains']  # 如果想精确查找去掉contains就行，列表里的字符串对应ORM语法

    action_list = [StarkHandler.action_multi_delete, ]

    # 以后尽量把数据封装到类中
    search_group = [
        Option('gender', is_multi=True),
        Option('depart', is_multi=True),
    ]

    # def save(self, form, is_update=False):
    #     form.instance.depart_id = 1  # 如果页面不想显示部门，可以在form表单保存之前，先给depart_id一个默认值
    #     form.save()


site.register(models.Department, DeaprtmentHandler)

site.register(models.UserInfo, UserInfoHandler)


class DeployHandler(StarkHandler):
    per_page_count = 1

    list_display = ['title', get_choice_text('状态', 'status'), StarkHandler.display_edit, StarkHandler.display_del]


site.register(models.Deploy, DeployHandler)
