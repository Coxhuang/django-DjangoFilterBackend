import django_filters
from app import models
from django.db.models import Q


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
