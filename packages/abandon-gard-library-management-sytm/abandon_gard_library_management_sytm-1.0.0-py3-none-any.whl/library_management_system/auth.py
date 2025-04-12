import msvcrt



# 密码加密显示
def jiami():
    print('请输入密码: ')
    li = []
    while True:
        ch = msvcrt.getch()
        if ch == b'\r':  # 回车
            break
        elif ch == b'\x08':  # 退格
            if li:
                li.pop()
                msvcrt.putch(b'\b')
                msvcrt.putch(b' ')
                msvcrt.putch(b'\b')
        # Esc
        elif ch == b'\x1b':
            break
        else:
            li.append(ch)
            msvcrt.putch(b'*')
    return b''.join(li).decode()


def register():
    print("开始进行用户注册")
    while True:
        reg_name = input("请输入注册用户名：\n")
        for i in sensitive_character:
            if i in reg_name:
                reg_name = reg_name.replace(i, '*')
                print("用户名包含非法字{}，请重新输入。".format(reg_name))
                break
        else:
            if reg_name in vip_name:
                print('该用户名已被注册！')
            else:
                break

    while True:
        reg_psw = jiami()
        if len(reg_psw) < 6:
            print('密码太简单!密码长度应为为6 - 18位!，请重新输入：')
            continue
        elif reg_psw.isalpha() or reg_psw.isdigit():
            print("请不要使用纯字母或纯数字密码，应该为数字字母混合密码，请重新输入：")
            continue
        else:
            person_info = {'name': reg_name, 'psw': reg_psw, 'is_admin': False}
            vip_info.append(person_info)
            vip_name.append(reg_name)
            print("恭喜，注册成功。")
            break


def login():
    print("开始进行用户登录")
    log_conut1 = 3
    while log_conut1:
        log_name = input("请输入用户名：\n")
        if log_name not in vip_name:
            log_conut1 -= 1
            print("用户名不存在，您还要{}次试错机会。".format(log_conut1))
            continue
        else:
            conut_log2 = 3
            while conut_log2:
                conut_log2 -= 1
                cur_index = vip_name.index(log_name)
                log_psw = jiami()
                if log_psw == vip_info[cur_index]['psw']:
                    print('登录成功!')
                    return vip_info[cur_index], vip_info[cur_index]['is_admin']
                else:
                    print("密码输入不正确。您还有{}次试错机会。".format(conut_log2))
    print("登录失败，试错机会已用完。")
    return None, False
# vip_info  系统内已注册用户信息表
vip_info = [
    {'name': '张三', 'psw': 'zs333333', 'is_admin': False},
    {'name': '李四', 'psw': 'ls444444', 'is_admin': False},
    {'name': 'admin', 'psw': 'admin123', 'is_admin': True}  # 管理员用户
]

# 用户名列表
vip_name = [vip_info[i]["name"] for i in range(len(vip_info))]

# 建立敏感词库
sensitive_character = ["傻", "屁", "草", "操", "垃圾", "z"]
