from auth import vip_info, vip_name


def add_user():
    print("开始添加用户")
    while True:
        reg_name = input("请输入新用户的用户名：\n")
        if reg_name in vip_name:
            print('该用户名已被注册！')
        else:
            break
    while True:
        reg_psw = input("请输入新用户的密码：\n")
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
            print("用户添加成功。")
            break


def delete_user():
    print("开始删除用户")
    user_name = input("请输入要删除的用户的用户名：\n")
    if user_name in vip_name:
        index = vip_name.index(user_name)
        del vip_info[index]
        vip_name.remove(user_name)
        print("用户删除成功。")
    else:
        print("该用户不存在。")


def modify_user():
    print("开始修改用户信息")
    user_name = input("请输入要修改信息的用户的用户名：\n")
    if user_name in vip_name:
        index = vip_name.index(user_name)
        new_psw = input("请输入新的密码（不修改请直接回车）：\n")
        if new_psw:
            vip_info[index]['psw'] = new_psw
            print("用户密码修改成功。")
    else:
        print("该用户不存在。")


def display_users():
    print("当前系统内的用户信息如下：")
    for user in vip_info:
        print(f"用户名：{user['name']}")


def admin_menu():
    while True:
        print("=" * 20)
        print("管理员用户信息维护菜单：")
        print("1. 添加用户")
        print("2. 删除用户")
        print("3. 修改用户信息")
        print("4. 显示用户信息")
        print("5. 退出维护菜单")
        choice = input("请输入您的选择（1 - 5）：")
        if choice == '1':
            add_user()
        elif choice == '2':
            delete_user()
        elif choice == '3':
            modify_user()
        elif choice == '4':
            display_users()
        elif choice == '5':
            print("退出用户信息维护菜单。")
            break
        else:
            print("输入无效，请输入 1 - 5 之间的数字。")
