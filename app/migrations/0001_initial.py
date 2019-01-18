# Generated by Django 2.0.7 on 2019-01-17 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='学生姓名')),
                ('createDate', models.DateTimeField(auto_now_add=True, verbose_name='用户创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='老师姓名')),
                ('createDate', models.DateTimeField(auto_now_add=True, verbose_name='用户创建时间')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='tea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.Teacher', verbose_name='老师'),
        ),
    ]
