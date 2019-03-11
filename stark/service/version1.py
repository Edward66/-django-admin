from django.urls import re_path
from django.shortcuts import HttpResponse


class StarkSite:
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, handler_class):
        """

        :param model_class: 是models中的数据库表对应的类。models.UserInfo
        :param handler_class: 处理请求的视图函数所在的类
        :return:
        """

        """
        self._registry = [
            {'model_class': model.Department,'handler':DepartmentHandler(models.Department)},
            {'model_class': model.UserInfo,'handler':UserInfo(models.UserInfo)}, 
            {'model_class': model.Host,'handler':Host(models.Host)},
        ]
        """

        self._registry.append({'model_class': model_class, 'handler': handler_class(model_class)})

    def get_urls(self):
        patterns = []
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']
            app_name = model_class._meta.app_label  # 获取当前类所在的app名称
            model_name = model_class._meta.model_name  # 获取当前类所在的表名称
            patterns.append(re_path(r'%s/%s/list' % (app_name, model_name,), handler.list_view))
            patterns.append(re_path(r'%s/%s/add' % (app_name, model_name,), handler.add_view))
            patterns.append(re_path(r'%s/%s/edit/(\d+)' % (app_name, model_name,), handler.edit_view))
            patterns.append(re_path(r'%s/%s/delete/(\d+)' % (app_name, model_name,), handler.delete_view))
            # <class 'app01.models.Department'>
            # /app01/department/list/
            # /app01/department/add/
            # /app01/department/edit/(\d+)/
            # /app01/department/del/(\d+)/

            # patterns.append(re_path(r'^x1/', lambda request: HttpResponse('1')), )
            # patterns.append(re_path(r'^x2/', lambda request: HttpResponse('1')), )

        return patterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace


"""
[

{'model_class': < class 'app01.models.Department' > ,'handler': 
< app01.stark.DeaprtmentHandler object at 0x1075aba20 >}, 

{'model_class': < class 'app01.models.UserInfo' > ,
'handler': < app01.stark.UserInfoHandler object at 0x1075abac8 >}, 

{'model_class': < class 'app02.models.Host' > ,
'handler': < app02.stark.HostHandler object at 0x1075abeb8 >}

]
"""

site = StarkSite()
