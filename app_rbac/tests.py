# 数据构造
menu_list = [
    {'id': 1, 'title': '菜单1'},
    {'id': 2, 'title': '菜单2'},
    {'id': 3, 'title': '菜单3'},
]

menu_dict = {}

"""
将menu_list变成menu_dict:
{
    1: "{'id': 1, 'title': '菜单1'}",
    2: "{'id': 2, 'title': '菜单2'}",
    3: "{'id': 3, 'title': '菜单3'}",
}
"""

for item in menu_list:
    menu_dict[item['id']] = item
print(menu_dict)
