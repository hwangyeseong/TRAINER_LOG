import json
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("data") / "members.json"

def load_members():
    """JSON 파일에서 회원 목록 불러오기"""

    if not DATA_FILE.exists():
        return []

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def save_members(members):
    """회원 목록을 JSON 파일에 저장"""

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            members,
            file,
            indent=4,
            ensure_ascii=False
        )

def register_member(members, user_id, name, password, email, phone):
    """회원 등록"""

    # 회원 ID 중복 확인
    for member in members:
        if member["user_id"] == user_id:
            return False

    # 새로운 회원 정보
    member = {
        "user_id" : user_id,
        "name": name,
        "password": password,
        "email": email,
        "phone": phone,
        "reg_date" : datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
    }

    # 회원 목록에 추가
    members.append(member)

    return True
