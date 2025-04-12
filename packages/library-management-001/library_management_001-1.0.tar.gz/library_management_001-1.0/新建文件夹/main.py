from login_register import register, login
from user_info_maintenance import add_user, delete_user, modify_user, display_user

# 系统内已注册用户信息表
vip_info = [
    {'name': '张三', 'psw': 'zs333333'},
    {'name': '李四', 'psw': 'ls444444'},
    {'name': '王五', 'psw': 'ww555555'},
    {'name': '周六', 'psw': 'zl666666'}
]
# 用户名列表
vip_name = [vip_info[i]["name"] for i in range(len(vip_info))]

# 欢迎界面
print("===========================")
print("欢迎使用图书馆借阅管理系统".center(18))
print("1 注册")
print("2 登录")
print("===========================")
flag = input("请输入（1 or 2）选择系统功能:")

# 注册
if flag == "1":
    vip_info, vip_name = register(vip_info, vip_name)
    if vip_info:
        login(vip_info, vip_name)

# 登录
elif flag == "2":
    if login(vip_info, vip_name):
        is_admin = input("请问您是否是管理员？(y/n)：")
        if is_admin.lower() == 'y':
            while True:
                print("1. 增加用户信息")
                print("2. 删除用户信息")
                print("3. 修改用户信息")
                print("4. 显示用户信息")
                print("5. 退出维护")
                choice = input("请输入您的选择(1-5)：")
                if choice == "1":
                    vip_info, vip_name = add_user(vip_info, vip_name)
                elif choice == "2":
                    vip_info, vip_name = delete_user(vip_info, vip_name)
                elif choice == "3":
                    vip_info, vip_name = modify_user(vip_info, vip_name)
                elif choice == "4":
                    display_user(vip_info)
                elif choice == "5":
                    print("退出用户信息维护页面。")
                    break
                else:
                    print("无效的选择，请重新输入。")
else:
    print("请输入数字1或者2！")