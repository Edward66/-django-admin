import functools
from types import FunctionType

from django.http import QueryDict
from django.urls import re_path
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render

from stark.utils.pagination import Pagination


def get_choice_text(title, field):
    """
    对于Stark组件中定义列时，choice如果想要显示中文信息，调用此方法即可
    :param title: 希望页面显示的表头
    :param field: 字段名称
    :return:
    """

    def wrapper(self, obj=None, is_header=None):
        if is_header:
            return title
        method = 'get_%s_display' % field
        return getattr(obj, method)()

    return wrapper


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
        self._registry.append(
            {'model_class': model_class, 'handler': handler_class(self, model_class, prev), 'prev': prev})

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
    per_page_count = 10
    has_add_btn = True

    def __init__(self, site, model_class, prev):
        self.site = site
        self.model_class = model_class
        self.prev = prev
        self.request = None

    def get_add_btn(self):
        if self.has_add_btn:
            return f'<a href="%s" class="btn btn-primary">添加</a>' % self.reverse_add_url()
        return None

    def display_edit(self, obj=None, is_header=None):
        """
        自定义页面显示的列（表头和内容）
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '编辑表头'
        name = '%s:%s' % (self.site.namespace, self.get_edit_url_name)  # stark:app01_userinfo_edit
        return mark_safe('<a href="%s">编辑</a>' % reverse(name, args=(obj.pk,)))

    def display_del(self, obj=None, is_header=None):
        if is_header:
            return '删除表头'
        name = '%s:%s' % (self.site.namespace, self.get_delete_url_name)
        return mark_safe('<a href="%s">删除</a>' % reverse(name, args=(obj.pk,)))

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

        # 1.处理分页
        all_count = self.model_class.objects.all().count()
        query_params = request.GET.copy()  # page=1&level=2
        # query_params._mutable = True  # 把_mutable变成True，才可以被修改page
        # query_params['page'] = 2
        pager = Pagination(
            current_page=request.GET.get('page'),
            all_count=all_count,
            base_url=request.path_info,
            query_params=query_params,
            per_page_data=self.per_page_count,
        )

        data_list = self.model_class.objects.all()[pager.start:pager.end]

        list_display = self.get_list_display()

        # 2. 处理表格的表头
        # 访问http://127.0.0.1:8000/stark/app01/userinfo/list
        # 页面上要显示的列，示例：['name', 'age', 'email']

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

        # 3. 处理表的内容 ['name','age']

        body_list = []
        for queryset_obj in data_list:
            print(queryset_obj)
            tr_list = []
            if list_display:
                for field_or_func in list_display:
                    if isinstance(field_or_func, FunctionType):
                        # field_or_func是函数（类调用的），所以要传递self
                        tr_list.append(field_or_func(self, queryset_obj, is_header=False))
                    else:
                        tr_list.append(getattr(queryset_obj, field_or_func))  # obj.depart
            else:
                tr_list.append(queryset_obj)
            body_list.append(tr_list)

        # 4.处理添加按钮
        add_btn = self.get_add_btn()

        context = {
            'data_list': data_list,
            'header_list': header_list,
            'body_list': body_list,
            'pager': pager,
            'add_btn': add_btn,
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

    def reverse_add_url(self):
        # 根据别名进行反向生成URL
        name = '%s:%s' % (self.site.namespace, self.get_add_url_name)
        base_url = reverse(name)
        if not self.request.GET:
            add_url = base_url
        else:
            params = self.request.GET.urlencode()
            new_query_dict = QueryDict(mutable=True)
            new_query_dict['_filter'] = params
            add_url = '%s?%s' % (base_url, new_query_dict.urlencode())
        return add_url

    def wrapper(self, func):  # 增删改查视图函数的时候，给self.request赋值request
        @functools.wraps(func)  # 保留原函数的原信息，写装饰器建议写上这个。
        def inner(request, *args, **kwargs):
            self.request = request
            return func(request, *args, **kwargs)

        return inner

    def get_urls(self):  # 先在传进来的handler里重写
        patterns = [
            re_path(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path(r'^edit/(\d+)/$', self.wrapper(self.edit_view), name=self.get_edit_url_name),
            re_path(r'^delete/(\d+)/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]
        patterns.extend(self.extra_urls())  # 先去传进来的handler里找
        return patterns

    def extra_urls(self):
        return []


site = StarkSite()
