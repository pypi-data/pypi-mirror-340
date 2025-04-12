import getpass

# 敏感词库
sensitive_words = ["傻", "蠢", "笨", "呆", "愚"]
# 存储用户信息
users = {}
# 存储管理员信息
admins = {"admin": "Admin123"}
# 错误登录次数
login_errors = {}


def has_sensitive_word(username):
    """检查用户名是否包含敏感词"""
    for word in sensitive_words:
        if word in username:
            masked_username = username.replace(word, "*" * len(word))
            print(f"{masked_username} 用户名不可注册，请重新输入。")
            return True
    return False


def is_valid_password(password):
    """检查密码是否符合要求"""
    if len(password) < 6:
        print("密码不可少于6位，请重新输入。")
        return False
    has_digit = any(char.isdigit() for char in password)
    has_alpha = any(char.isalpha() for char in password)
    if not (has_digit and has_alpha):
        print("密码不可为纯数字或纯字母，应至少为字母+数字的混合，请重新输入。")
        return False
    return True


def register():
    """用户注册功能"""
    while True:
        username = input("请输入要注册的用户名：")
        if has_sensitive_word(username):
            continue
        while True:
            password = getpass.getpass("请输入要注册的密码：")
            if is_valid_password(password):
                users[username] = password
                print("注册成功！")
                return


def login():
    """用户登录功能"""
    username = input("请输入要登录的用户名：")
    if username not in users and username not in admins:
        print("用户未注册，请先注册。")
        return
    if username in login_errors and login_errors[username] >= 3:
        print("登录错误次数过多，禁止登录本系统。")
        return
    for i in range(3):
        password = getpass.getpass("请输入要登录的密码：")
        if (username in users and users[username] == password) or (
                username in admins and admins[username] == password
        ):
            print("登录成功！")
            if username in admins:
                return True
            return False
        else:
            if username not in login_errors:
                login_errors[username] = 1
            else:
                login_errors[username] += 1
            if login_errors[username] >= 3:
                print("登录错误次数过多，禁止登录本系统。")
                return
            print(f"用户名或密码错误，你还有 {2 - i} 次机会。")


def welcome():
    """系统欢迎界面"""
    print("欢迎使用图书馆借阅管理系统！")
    while True:
        choice = input("请选择操作：1. 注册  2. 登录  3. 退出：")
        if choice == "1":
            register()
        elif choice == "2":
            is_admin = login()
            if is_admin is not None:
                return is_admin
        elif choice == "3":
            print("感谢使用，再见！")
            return None
        else:
            print("输入无效，请重新输入。")