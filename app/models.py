from django.db import models

class Teacher(models.Model):
    """老师表"""
    name = models.CharField(verbose_name="老师姓名",max_length=16)
    createDate = models.DateTimeField(verbose_name="用户创建时间",auto_now_add=True)
    salary = models.IntegerField(verbose_name="薪资",default=0)

class Student(models.Model):
    """学生表"""
    tea = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING,verbose_name="老师")
    name = models.CharField(verbose_name="学生姓名",max_length=16)
    createDate = models.DateTimeField(verbose_name="用户创建时间",auto_now_add=True)

