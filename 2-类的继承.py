"""
类的继承：
————继承，为了提高代码的复用性。
————接口，1.API(网站);
         2.用于做约束的数据类型（python中不存在，Java/C#....存在）

         # Java中的约束示例：约束 -- 实现了类的成员的约束
            Interface IFoo{
                function send(){
                   可以定义一个方法，但是不能写任何代码
                }
            }

            class Foo(IFoo){  称为 “实现” 了 IFoo 的接口，则类中必须写完IFoo中的所有方法
                function send(){
                    ......
                }
            }

            function func(IFoo object){
                obj.send()  称为实现了IFoo类的对象
            }

    #### 对于Java中的类，只能继承一个类，只能支持单继承，但是支持实现多个接口 ####
    #### 也就是说类可以继承多个接口，但是只能继承一个类 ####

————抽象，抽象类、抽象方法。用于做约束（python、Java、C# 都有）
        既能做约束，又能提供公共功能
        Java代码：
        abstract class Foo(){
            function f1(){                    普通方法
                System.Out.PrintLine('f1')
            }

            abstract function f2(){            在抽象类中定义了一个抽象方法
                pass                            抽象方法中不允许写代码
            }
        }

        class Bar(Foo){
            function f2(){                      继承了Foo类，那么必须写上Foo类中的所有方法，否则编译不通过
                System.Out.PrintLine('f1')
            }
        }

        在python中：
"""

import abc


class Foo(metaclass=abc.ABCMeta):  # 抽象类
    def f1(self):
        print('123')

    @abc.abstractmethod
    def f2(self):  # 抽象类中定义抽象方法
        pass


class Bar(Foo):
    pass


# 未实现抽象类中的抽象方法，实例化的时候会报错
# Can't instantiate abstract class Bar with abstract methods f2

obj = Bar()  # 编译不通过


#### python中一种不太巧妙的机制：通过异常实现约束（源码中使用到多一些） ###

class Foo(metaclass=abc.ABCMeta):  # 抽象类
    def f1(self):
        print('123')

    def f2(self):  # 抽象类中定义抽象方法
        raise NotImplementedError()  # 异常约束


class Bar(Foo):
    pass


obj = Bar()  # 编译通过
obj.f2()  # 编译不通过--报错！


# 由于语言不同，Java的约束更棒！java是编译型语言，python是解释性语言，如果出现错误，编译直接不通过。