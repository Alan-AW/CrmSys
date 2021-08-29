"""
popup:
    主页面（要开启popup的页面）
        绑定事件，出发pop()函数：
        function pop() {
        window.open('add/city/', 'name', 'status=1, height=700, width=700, toolbar=0, resizeable=0');
    }
        open() 中的参数 'name' 如果一致，那么只会弹出一个窗口，不一致则open几次就打开几次。

    popup页面（被弹出的页面）：
        <form method="post">
            {% csrf_token %}
            <input type="text" id="input" name="city">
            <input type="submit" value="提交">
        </form>

    后端返回页面：
        自执行函数（用于做隔离）
        什么是隔离：假设有一个基于jquery开发的组件的js文件中与其他的js文件写了同名函数，那么会出现漏洞，使用自执行函数就可以在
        函数内编写其他的函数，使用的时候自己调用即可，例：

        (
        function (jq) {
            const obj = 1;
            function a() {

            }
            function b() {

            }
            function c() {
                a();
                b();
            }
        }
        )(jQuery)

        (function (status, cityId, cityName) {
            opener.addStatus(status, cityId, cityName);   反向调用打开popup页面内的方法
            window.close();
	    })('success!',{{ cityId }}, '{{ cityName }}');

"""
