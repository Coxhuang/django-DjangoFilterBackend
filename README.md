

# django-filters


## #0 GitHub

```
https://github.com/Coxhuang/django-DjangoFilterBackend.git
```


## #1 环境

```
Django==2.0.7
djangorestframework==3.8.2
django-filter==2.0.0
```

## #2 需求

- 获取某些数据时,需要按某些字段过滤
- 过滤时,有些的字段是 "跨表" 的字段,该如何处理
- 过滤时,有些字段是 "区间" 字段(比如时间),该如何处理
- 过滤时,有些字段是 "跨表" 后的 "区间" 字段,又该如何处理


## #3 起步

### #3.1 新建一个Django项目

```
.
├── app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── filters.py      # 添加新文件
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── db.sqlite3
├── djangofilters
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── templates
```
### #3.2 settings.py

```
INSTALLED_APPS = [
    ...
    'rest_framework',
    'django_filters',
    'app',
]
```
### #3.3 models.py


```
from django.db import models
class Teacher(models.Model):
    """老师表"""
    name = models.CharField(verbose_name="老师姓名",max_length=16)
class Student(models.Model):
    """学生表"""
    tea = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING,verbose_name="老师")
    name = models.CharField(verbose_name="学生姓名",max_length=16)

```





## #4 django REST框架简单的过滤

### #4.1 没有使用过滤

```
class getUserListSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    teaname = serializers.CharField(label="老师姓名",source="tea.name")
    class Meta:
        model = models.Student
        fields = ["id","name","teaname",]
class getUserListView(mixins.ListModelMixin,GenericViewSet):
    queryset = models.Student.objects.all()
    serializer_class = getUserListSerializer
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/2019011801054990.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NveGh1YW5n,size_16,color_FFFFFF,t_70)

### #4.2 加入过滤器

filters.py

```
import django_filters
from app import models
class getUserListFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = models.Student
        fields = ["name",]

```
views.py
```
...
from django_filters import rest_framework
from app.filters import getUserListFilter

class getUserListView(mixins.ListModelMixin,GenericViewSet):
    ...
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filter_class = getUserListFilter
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190118010632529.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NveGh1YW5n,size_16,color_FFFFFF,t_70)


![在这里插入图片描述](https://img-blog.csdnimg.cn/20190118010456385.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NveGh1YW5n,size_16,color_FFFFFF,t_70)

## #5 跨表过滤

需求:根据老师的名字过滤


```
class getUserListFilter(django_filters.rest_framework.FilterSet):
    teaname = django_filters.CharFilter(field_name='tea__name', label="老师姓名") # 跨表操作
    class Meta:
        model = models.Student
        fields = ["name","teaname",]
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190118010814352.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NveGh1YW5n,size_16,color_FFFFFF,t_70)


![在这里插入图片描述](https://img-blog.csdnimg.cn/20190118010845187.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NveGh1YW5n,size_16,color_FFFFFF,t_70)
## #6 区间过滤

- 新增字段createDate(用户创建时间)

```
createDate = models.DateTimeField(verbose_name="用户创建时间",auto_now_add=True)
```


filters.py
```
class getUserListFilter(django_filters.rest_framework.FilterSet):
    teaname = django_filters.CharFilter(field_name='tea__name', label="老师姓名")
    RegDate = django_filters.DateFromToRangeFilter(field_name='createDate', lookup_expr='gte', label='注册时间') # 区间过滤
    class Meta:
        model = models.Student
        fields = ["name","teaname","RegDate",]
```
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190118012111661.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NveGh1YW5n,size_16,color_FFFFFF,t_70)


![在这里插入图片描述](https://img-blog.csdnimg.cn/20190118012211577.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NveGh1YW5n,size_16,color_FFFFFF,t_70)


**注意** : 在url的参数中,原来我们在filters.py中定义的变量是 "RegDate",到了url中变成了 "RegDate_after" 和 "RegDate_before",这是框架给我设定好的区间变量,直接使用就行

**more** : 更多关键词,请参考文档


## #7 跨表后区间过滤

需求:学生老师的薪资范围过滤

- 新增字段salary(老师薪资)

filters.py

```
class getUserListFilter(django_filters.rest_framework.FilterSet):
    teaname = django_filters.CharFilter(field_name='tea__name', label="老师姓名")
    RegDate = django_filters.DateFromToRangeFilter(field_name='createDate', lookup_expr='gte', label='注册时间')
    salary = django_filters.RangeFilter(method='salary_filter', label='薪资',)
    class Meta:
        model = models.Student
        fields = ["name","teaname","RegDate","salary"]

    def salary_filter(self, queryset, name, value):

        return queryset.filter(Q(tea__salary__gte = int(value.start)) &
                               Q(tea__salary__lte = int(value.stop)))
```

### #7.1 格式
- 声明

```
salary = django_filters.RangeFilter(method='salary_filter', label='薪资',)
```

- 函数

```
 def salary_filter(self, queryset, name, value):
        return queryset.filter(Q(tea__salary__gte = int(value.start)) &
                               Q(tea__salary__lte = int(value.stop)))
```

- 细节
1. 函数名必须是 method 的值
2. 如果是区间,可以使用django_filters.RangeFilter,如果不是区间可以使用其他
3. 重写函数时,里面的参数不会自动补全

- 坑
1. 使用Q时,一定不能使用or / and,只能使用 | & 
2. return 的数值,如果使用queryset.filter(xxx).filter(xxx),那么返回的结果是所有过滤的交集,如果每个自定义函数都返回自己过滤的数据(例如,models.Student.objects.filter().filter()),那么过滤的结果是所有符合条件的并集
3. value的正确使用,value.start对应的是url中的min(salary_min),value.stop对应url的max(salary_max)
![在这里插入图片描述](https://img-blog.csdnimg.cn/20190119002001423.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NveGh1YW5n,size_16,color_FFFFFF,t_70)


![在这里插入图片描述](https://img-blog.csdnimg.cn/20190119002035923.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L0NveGh1YW5n,size_16,color_FFFFFF,t_70)
