import auth
import admin

# 欢迎界面
welcome = ["===========================",
           "欢迎使用图书馆借阅管理系统",
           "1 注册",
           "2 登录",
           "3 退出系统",
           "==========================="]
for i in welcome:
    print("%s" % i.center(18, "　"))

while True:
    flag = input("请输入（1、2 或 3）选择系统功能:")
    if flag == "1":
        auth.register()
    elif flag == "2":
        user, is_admin = auth.login()
        if user:
            if is_admin:
                admin.admin_menu()
            else:
                print("普通用户登录成功，暂无其他操作，可选择退出系统。")
    elif flag == "3":
        print("感谢使用，再见！")
        break
    else:
        print("请输入有效的数字（1、2 或 3）！")
