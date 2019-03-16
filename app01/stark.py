from stark.service.version1 import site
from stark.service.version1 import StarkHandler, get_choice_text

from app01 import models


class DeaprtmentHandler(StarkHandler):
    has_add_btn = True

    list_display = ['id', 'title', StarkHandler.display_edit, StarkHandler.display_del]


class UserInfoHandler(StarkHandler):
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

    per_page_count = 1

    has_add_btn = True


site.register(models.Department, DeaprtmentHandler)

site.register(models.UserInfo, UserInfoHandler)
