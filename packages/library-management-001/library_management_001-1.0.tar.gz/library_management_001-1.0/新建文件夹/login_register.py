from password_encryption import jiami

# 敏感词库
sensitive_character = ["傻", "蠢", "笨", "呆", "愚"]


# 注册功能
def register(vip_info, vip_name):
    print("开始进行用户注册")
    reg_name = input("请输入注册用户名：\n")
    for i in sensitive_character:
        while i in reg_name:
            reg_name = reg_name.replace(i, '*')
            print(f"用户名包含非法字{i}，请重新输入。")
            reg_name = input("请输入注册用户名：\n")

    if reg_name in vip_name:
        print('该用户名已被注册！')
    else:
        while True:
            reg_psw = jiami()
            print()
            if len(reg_psw) < 6:
                print('密码太简单!密码长度应为为6-18位!，请重新输入：')
            elif reg_psw.isalpha() or reg_psw.isdigit():
                print("请不要使用纯字母或纯数字密码，应该为数字字母混合密码，请重新输入：")
            else:
                person_info = {"name": reg_name, "psw": reg_psw}
                vip_info.append(person_info)
                vip_name.append(reg_name)
                print("恭喜，注册成功。")
                break
    return vip_info, vip_name


# 登录功能
def login(vip_info, vip_name):
    print("开始进行用户登录")
    log_conut1 = 3
    while log_conut1:
        log_name = input("请输入用户名：\n")
        if log_name not in vip_name:
            log_conut1 -= 1
            print(f"用户名不存在，您还要{log_conut1}次试错机会。")
            continue
        else:
            conut_log2 = 3
            while conut_log2:
                conut_log2 -= 1
                cur_index = vip_name.index(log_name)
                log_psw = jiami()
                print()
                if log_psw == vip_info[cur_index]['psw']:
                    print('登录成功!跳转到《图书馆借阅管理系统》使用页面...')
                    return True
                else:
                    print(f"密码输入不正确。您还有{conut_log2}次试错机会。")
            break
    return False