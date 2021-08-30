from django import forms


class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """
        统一添加样式,使用的时候直接在form类中继承这个类即可，因为这个类已经继承了一个 forms.ModelForm 这个基类，
        再次继承这个类的话也会继承这个基类，并且同时继承了这个类的所有方法
        :param args:
        :param kwargs:
        """
        super(BootStrapModelForm, self).__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs['class'] = 'form-control'
