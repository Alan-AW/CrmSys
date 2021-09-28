## **STARK组件:**帮助开发者对数据表快速进行 增删改查+ 的功能组件

## 一、通过Model类获取到app名称和表名称

```python
model_class = models.UserInfo.objects.all()  # model类对象

app_label, model_label = model_class._meta.app_label, model_class._meta.model_label
"""
app_label: model_class._meta.app_label
model_label: model_class._meta.model_label
"""
```

