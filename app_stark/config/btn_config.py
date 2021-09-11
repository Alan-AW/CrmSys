"""
对于业务中的各项数据表判断是否拥有权限进行增删改的操作
可以在配置中直接先继承该类，然后继承StarkHandler即可
"""

from django.conf import settings
from app_stark.service.StarkModular import StarkHandler


class BaseBtn(object):
    # 粒度控制到按钮设置
    def get_add_btn(self):
        name = '%s:%s' % (self.site.namespace, self.get_add_url_name)
        if name in self.request.session.get(settings.PERMISSION_SESSION_KEY):
            return super().get_add_btn()
        return None

    # 检查是否有相应的 编辑和删除 权限
    def get_list_display(self):
        val = super().get_list_display()
        permission_dict = self.request.session.get(settings.PERMISSION_SESSION_KEY)
        edit_name = '%s:%s' % (self.site.namespace, self.get_edit_url_name)
        del_name = '%s:%s' % (self.site.namespace, self.get_delete_url_name)
        if edit_name not in permission_dict:
            val.remove(StarkHandler.display_edit)
        if del_name not in permission_dict:
            val.remove(StarkHandler.display_del)
        return val
