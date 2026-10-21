from member.meber_service import (
    load_members,
    save_members,
    register_member
    )

def main():
    members = load_members()

    print("\n===== 회원 등록 =====")

    user_id = input("회원 ID: ")
    name = input("이름: ")
    password = input("비밀번호: ")
    email = input("이메일: ")
    phone = input("연락처: ")

    result = register_member(
        members,
        user_id,
        name,
        password,
        email,
        phone
    )

    if result == True:
        save_members(members)
        print("회원 등록 완료")
    else:
        print("이미 등록된 회원 ID입니다.")

if __name__ == "__main__":
    main()