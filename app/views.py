from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from app import models
from rest_framework import serializers
from drf_dynamic_fields import DynamicFieldsMixin
from django_filters import rest_framework
from rest_framework import filters
from app.filters import getUserListFilter

"""
1. 获取学生列表
"""


class getUserListSerializer(DynamicFieldsMixin,serializers.ModelSerializer):
    teaname = serializers.CharField(label="老师姓名",source="tea.name")
    salary = serializers.IntegerField(label="老手薪资",source="tea.salary")
    class Meta:
        model = models.Student
        fields = ["id","name","teaname","salary",]

class getUserListView(mixins.ListModelMixin,GenericViewSet):
    queryset = models.Student.objects.all()
    serializer_class = getUserListSerializer
    filter_backends = (rest_framework.DjangoFilterBackend,)
    filter_class = getUserListFilter
