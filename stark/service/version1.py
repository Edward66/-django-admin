from types import FunctionType

from django.urls import re_path
from django.shortcuts import HttpResponse, render


class StarkSite:
    def __init__(self):
        self._registry = []
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model_class, handler_class=None, prev=None):
        """
        :param model_class: 是models中的数据库表对应的类。models.UserInfo
        :param handler_class: 处理请求的视图函数所在的类
        :param prev: 生成URL的前缀
        :return:
        """
        if not handler_class:
            handler_class = StarkHandler
        self._registry.append({'model_class': model_class, 'handler': handler_class(model_class, prev), 'prev': prev})

        """
        self._registry = [
            {'prev':'None',model_class': model.Department,'handler':DepartmentHandler(models.Department,prev)对象中有一个model_class=models.Department},
            {'prev':'private','model_class': model.UserInfo,'handler':UserInfo(models.UserInfo,prev)对象中有一个model_class=models.UserInfo}, 
            {'prev':'None','model_class': model.Host,'handler':Host(models.Host,prev)对象中有一个model_class=models.Host},
        ]
        """

    def get_urls(self):
        patterns = []
        for item in self._registry:
            model_class = item['model_class']
            handler = item['handler']  # 实例化了StarkHandler，hanlder是StarkHandler的对象
            prev = item['prev']
            app_name = model_class._meta.app_label  # 获取当前类所在的app名称
            model_name = model_class._meta.model_name  # 获取当前类所在的表名称

            if prev:
                patterns.append(
                    re_path(r'^%s/%s/%s/' % (app_name, model_name, prev,), (handler.get_urls(), None, None))
                )
            else:
                patterns.append(
                    re_path(r'^%s/%s/' % (app_name, model_name,), (handler.get_urls(), None, None))
                )

        return patterns

    @property
    def urls(self):
        return self.get_urls(), self.app_name, self.namespace


class StarkHandler:
    list_display = []

    def __init__(self, model_class, prev):
        self.model_class = model_class
        self.prev = prev

    def get_list_display(self):
        """
        获取页面上应该显示的列,自定义扩展，列如：根据用户的不同来显示不同的列
        :return:
        """
        values = []
        values.extend(self.list_display)

        return values

    def list_view(self, request):
        """
        列表页面
        :param request:
        :return:
        """
        # 访问http://127.0.0.1:8000/stark/app01/userinfo/list : <class 'app01.models.UserInfo'>
        # 访问http://127.0.0.1:8000/stark/app02/host/list : <class 'app02.models.Host'>
        # self.model_class是不一样的

        # 1. 处理表格的表头
        # 访问http://127.0.0.1:8000/stark/app01/userinfo/list
        # 页面上要显示的列，示例：['name', 'age', 'email']

        list_display = self.get_list_display()

        header_list = []
        if list_display:
            for field_or_func in list_display:  # self.model_class._meta.get_field()拿到的是数据库里的一个字段
                if isinstance(field_or_func, FunctionType):
                    verbose_name = field_or_func(self, obj=None, is_header=True)
                    header_list.append(verbose_name)
                else:
                    verbose_name = self.model_class._meta.get_field(field_or_func).verbose_name
                    header_list.append(verbose_name)
        else:
            header_list.append(self.model_class._meta.model_name)  # 没有定义list_display，让表头显示表名称

        # 用户访问的表  models.UserInfo

        # 2. 处理表的内容 ['name','age']

        data_list = self.model_class.objects.all()

        '''
        [
            ['edward',28,],
            ['mark' 18,],
        ]
        '''

        body_list = []
        for queryset_obj in data_list:
            tr_list = []
            if list_display:
                for field_or_func in list_display:
                    if isinstance(field_or_func, FunctionType):
                        # field_or_func是函数（类调用的），所以要传递self
                        tr_list.append(field_or_func(self, queryset_obj, is_header=False))
                    else:
                        tr_list.append(getattr(queryset_obj, field_or_func))
            else:
                tr_list.append(queryset_obj)
            body_list.append(tr_list)

        context = {
            'data_list': data_list,
            'header_list': header_list,
            'body_list': body_list,
        }

        return render(request, 'stark/data_list.html', context)

    def add_view(self, request):
        """
        添加页面
        :param request:
        :return:
        """
        return HttpResponse('添加页面')

    def edit_view(self, request, pk):
        """
        编辑页面
        :param request:
        :param pk:
        :return:
        """
        return HttpResponse('编辑页面')

    def delete_view(self, request, pk):
        """
        删除页面
        :param request:
        :param pk:
        :return:
        """
        return HttpResponse('删除页面')

    def get_url_name(self, crud):
        app_name, model_name = self.model_class._meta.app_label, self.model_class._meta.model_name
        if self.prev:
            return "%s_%s_%s_%s" % (app_name, model_name, self.prev, crud)
        return "%s_%s_%s" % (app_name, model_name, crud)

    @property
    def get_list_url_name(self):
        """
        获取列表页面URL的name
        :return:
        """
        return self.get_url_name('list')

    @property
    def get_add_url_name(self):
        """
        获取添加页面URL的name
        :return:
        """
        return self.get_url_name('add')

    @property
    def get_edit_url_name(self):
        """
        获取修改页面URL的name
        :return:
        """
        return self.get_url_name('edit')

    @property
    def get_delete_url_name(self):
        """
        获取删除页面URL的name
        :return:
        """
        return self.get_url_name('delete')

    def get_urls(self):  # 先在传进来的handler里重写
        patterns = [
            re_path(r'^list/$', self.list_view, name=self.get_list_url_name),
            re_path(r'^add/$', self.add_view, name=self.get_add_url_name),
            re_path(r'^edit/(\d+)/$', self.edit_view, name=self.get_edit_url_name),
            re_path(r'^delete/(\d+)/$', self.delete_view, name=self.get_delete_url_name),
        ]
        patterns.extend(self.extra_urls())  # 先去传进来的handler里找
        return patterns

    def extra_urls(self):
        return []


site = StarkSite()
