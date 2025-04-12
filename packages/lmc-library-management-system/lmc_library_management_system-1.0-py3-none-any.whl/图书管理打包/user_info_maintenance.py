from login_register import users


def add_user():
    """增加用户信息"""
    username = input("请输入要添加的用户名：")
    if username in users:
        print("该用户已存在。")
    else:
        password = input("请输入要添加用户的密码：")
        users[username] = password
        print("用户添加成功。")


def delete_user():
    """删除用户信息"""
    username = input("请输入要删除的用户名：")
    if username in users:
        del users[username]
        print("用户删除成功。")
    else:
        print("该用户不存在。")


def modify_user():
    """修改用户信息"""
    username = input("请输入要修改的用户名：")
    if username in users:
        new_password = input("请输入新密码：")
        users[username] = new_password
        print("用户信息修改成功。")
    else:
        print("该用户不存在。")


def display_users():
    """显示所有用户信息"""
    if not users:
        print("暂无用户信息。")
    else:
        print("所有用户信息如下：")
        for username, password in users.items():
            print(f"用户名：{username}，密码：{password}")


def user_info_maintenance():
    """用户信息维护页面"""
    while True:
        print("用户信息维护页面")
        print("1. 增加用户信息")
        print("2. 删除用户信息")
        print("3. 修改用户信息")
        print("4. 显示用户信息")
        print("5. 退出")
        choice = input("请选择操作：")
        if choice == "1":
            add_user()
        elif choice == "2":
            delete_user()
        elif choice == "3":
            modify_user()
        elif choice == "4":
            display_users()
        elif choice == "5":
            print("退出用户信息维护页面。")
            break
        else:
            print("输入无效，请重新输入。")

