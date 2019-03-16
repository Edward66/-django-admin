from stark.service.version1 import site
from stark.service.version1 import StarkHandler, get_choice_text

from app01 import models


class DeaprtmentHandler(StarkHandler):
    list_display = ['id', 'title', StarkHandler.display_edit, StarkHandler.display_del]


class UserInfoHandler(StarkHandler):
    per_page_count = 1

    def display_gender(self, obj, is_header=None):
        if is_header:
            return '性别'
        return obj.get_gender_display()  # 对于choice字段，可以通过这个方法获取字符串

    def display_classes(self, obj, is_header=None):
        if is_header:
            return '班级'
        return obj.get_classes_display()

    # depart：foreign_key用__str__显示（在models里定义）
    list_display = [
        'name',
        get_choice_text('性别', 'gender'),
        get_choice_text('班级', 'classes'),
        'age',
        'email',
        'depart',
        StarkHandler.display_edit,
        StarkHandler.display_del
    ]


site.register(models.Department, DeaprtmentHandler)

site.register(models.UserInfo, UserInfoHandler)
