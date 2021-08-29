from django.db import models


class Depart(models.Model):
    title = models.CharField(max_length=32)


class User(models.Model):
    name = models.CharField(max_length=32)


class User1(User):
    email = models.EmailField(max_length=64)


"""
在以上三张表中：
Depart 表会生成 两个字段 -- id、title
User 表会生成 两个字段 -- id、name
user1 表会生成 一个字段 -- email 和 一个 user_ptr_id integer
    user_ptr_id integer 是django的一个组件，在内部会与User表生成一个关联
"""


######### 类的嵌套 #########

class Foo(object):
    x = 123

    def func(self):
        pass

    class Bar(object):
        x = 456


x1 = Foo()
print(x1.x)  # 123
print(x1.Bar.x)  # 456


####### Django的Orm中提供的一个功能 #######

class User(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        abstract = True

# 如果一个类中 写上了一个配置 abstract = True 表示数据库不生成这张表，这个类是用来给别的类进行继承使用的
# 应用场景： 权限系统
