from login_register import welcome
from user_info_maintenance import user_info_maintenance


def main():
    is_admin = welcome()
    if is_admin:
        user_info_maintenance()


if __name__ == "__main__":
    main()
