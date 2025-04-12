# 用户信息维护功能（管理员）
def add_user(vip_info, vip_name):
    print("开始增加用户信息")
    new_name = input("请输入新用户名：\n")
    if new_name in vip_name:
        print('该用户名已存在！')
    else:
        new_psw = input("请输入新用户密码：\n")
        new_user = {"name": new_name, "psw": new_psw}
        vip_info.append(new_user)
        vip_name.append(new_name)
        print("用户添加成功。")
    return vip_info, vip_name


def delete_user(vip_info, vip_name):
    print("开始删除用户信息")
    del_name = input("请输入要删除的用户名：\n")
    if del_name in vip_name:
        index = vip_name.index(del_name)
        del vip_info[index]
        vip_name.remove(del_name)
        print("用户删除成功。")
    else:
        print('该用户名不存在！')
    return vip_info, vip_name


def modify_user(vip_info, vip_name):
    print("开始修改用户信息")
    mod_name = input("请输入要修改的用户名：\n")
    if mod_name in vip_name:
        index = vip_name.index(mod_name)
        new_name = input("请输入新用户名（不修改请按回车）：\n")
        if new_name:
            vip_info[index]['name'] = new_name
            vip_name[vip_name.index(mod_name)] = new_name
        new_psw = input("请输入新密码（不修改请按回车）：\n")
        if new_psw:
            vip_info[index]['psw'] = new_psw
        print("用户信息修改成功。")
    else:
        print('该用户名不存在！')
    return vip_info, vip_name


def display_user(vip_info):
    print("显示所有用户信息")
    for user in vip_info:
        print(f"用户名：{user['name']}，密码：{user['psw']}")
    return vip_info