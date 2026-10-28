
# workout_crud.py

import json
from datetime import datetime
from pathlib import Path


class WorkoutCRUD:
    def __init__(self, member_dir):
        # data/members 폴더
        self.member_dir = Path(member_dir)

    # ==========================================
    # 1. 파일 경로 및 데이터 처리
    # ==========================================

    def get_folder(self, user_id):
        return self.member_dir / user_id

    def get_path(self, user_id):
        return self.get_folder(user_id) / "workouts.json"

    def get_user_id(self, member):
        return member["아이디"]

    def get_user_name(self, member):
        return member["이름"]

    def read_data(self, user_id):
        path = self.get_path(user_id)

        if not path.exists():
            return []

        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                print("운동 기록 파일의 형식이 올바르지 않습니다.")
                return None

            return data

        except (OSError, json.JSONDecodeError) as error:
            print(f"운동 기록 읽기 오류: {error}")
            return None

    def write_data(self, user_id, workouts):
        try:
            folder = self.get_folder(user_id)
            folder.mkdir(parents=True, exist_ok=True)

            with open(self.get_path(user_id), "w", encoding="utf-8") as file:
                json.dump(
                    workouts,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            return True

        except (OSError, TypeError, ValueError) as error:
            print(f"운동 기록 저장 오류: {error}")
            return False

    # ==========================================
    # 2. 목록 선택 및 페이지 이동
    # ==========================================

    def select_page(self, items, title, page_size=10):
        if not items:
            print("선택할 항목이 없습니다.")
            return None

        page = 0
        max_page = (len(items) - 1) // page_size

        while True:
            start = page * page_size
            end = min(start + page_size, len(items))

            print(f"\n========== {title} ==========")
            print(f"페이지 {page + 1} / {max_page + 1}")

            for index in range(start, end):
                print(f"{index + 1}. {items[index]}")

            print("------------------------------------")
            print("< 이전 | > 다음 | 0 취소")

            choice = input("번호 선택: ").strip()

            if choice == "<":
                if page > 0:
                    page -= 1
                else:
                    print("첫 번째 페이지입니다.")

            elif choice == ">":
                if page < max_page:
                    page += 1
                else:
                    print("마지막 페이지입니다.")

            elif choice == "0":
                return None

            elif choice.isdigit():
                number = int(choice)

                if start + 1 <= number <= end:
                    return number - 1

                print("현재 페이지에 표시된 번호를 선택해주세요.")

            else:
                print("올바른 번호를 입력해주세요.")

    # ==========================================
    # 3. 운동 기록 출력
    # ==========================================

    def get_set_list(self, record):
        sets = record.get("sets", [])

        # 새로운 JSON 형식
        if isinstance(sets, list):
            return sets

        # 이전 JSON 형식 지원
        try:
            count = int(sets)
            weight = float(record.get("weight", 0))
            reps = int(record.get("reps", 0))

            return [
                {
                    "set": index,
                    "weight": weight,
                    "reps": reps
                }
                for index in range(1, count + 1)
            ]

        except (ValueError, TypeError):
            return []

    def print_workout_record(self, record):
        print("\n" + "=" * 50)
        print(f"기록 번호: {record.get('record_id', '-')}")
        print(f"아이디: {record.get('user_id', '')}")
        print(f"운동 날짜: {record.get('date', '')}")
        print(f"운동 종목: {record.get('exercise', '')}")
        print("-" * 50)

        set_list = self.get_set_list(record)
        total_volume = 0

        for index, item in enumerate(set_list, start=1):
            weight = float(item.get("weight", 0))
            reps = int(item.get("reps", 0))
            volume = weight * reps

            total_volume += volume

            print(
                f"{index}세트 | "
                f"{weight:g}kg | "
                f"{reps}회 | "
                f"볼륨 {volume:,.1f}kg"
            )

        print("-" * 50)
        print(f"총 세트: {len(set_list)}세트")
        print(f"총 볼륨: {total_volume:,.1f}kg")
        print("=" * 50)

    # ==========================================
    # 4. 운동 종목 선택
    # ==========================================

    def select_exercise(self):
        machine_path = self.member_dir.parent / "muscles.json"

        if not machine_path.exists():
            print("muscles.json 파일이 없습니다.")
            return None

        try:
            with open(machine_path, "r", encoding="utf-8") as file:
                body_list = json.load(file)

        except (OSError, json.JSONDecodeError) as error:
            print(f"운동 종목 읽기 오류: {error}")
            return None

        if not isinstance(body_list, list):
            print("운동 종목 데이터 형식이 올바르지 않습니다.")
            return None

        muscle_list = [
            "Core",
            "Back",
            "Chest",
            "Shoulders",
            "Arms",
            "Legs"
        ]

        muscle_index = self.select_page(
            muscle_list,
            "운동 부위 선택"
        )

        if muscle_index is None:
            return None

        selected_muscle = muscle_list[muscle_index]

        exercise_list = []

        for body in body_list:
            if not isinstance(body, dict):
                continue

            if body.get("muscle") == selected_muscle:
                machines = body.get("machines", [])

                if isinstance(machines, list):
                    exercise_list.extend(machines)

        exercise_index = self.select_page(
            exercise_list,
            f"{selected_muscle} 운동 종목 선택"
        )

        if exercise_index is None:
            return None

        return exercise_list[exercise_index]

    # ==========================================
    # 5. 운동 기록 등록
    # ==========================================

    def register_workout(self, member):
        print("\n========== 운동 기록 등록 ==========")

        user_id = self.get_user_id(member)
        user_name = self.get_user_name(member)

        print(f"회원 이름: {user_name}")
        print(f"아이디: {user_id}")

        date = input("운동 날짜(YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")

        except ValueError:
            print("날짜 형식이 올바르지 않습니다.")
            return

        workouts = self.read_data(user_id)

        if workouts is None:
            return

        count = 0

        while True:
            exercise = self.select_exercise()

            if exercise is None:
                break

            set_list = []

            while True:
                set_number = len(set_list) + 1

                print(f"\n----- {set_number}세트 -----")

                try:
                    weight = float(input("무게(kg): "))
                    reps = int(input("반복 횟수: "))

                except ValueError:
                    print("숫자만 입력해주세요.")
                    continue

                if weight < 0 or reps <= 0:
                    print("무게는 0 이상, 횟수는 1 이상이어야 합니다.")
                    continue

                set_list.append({
                    "set": set_number,
                    "weight": weight,
                    "reps": reps
                })

                more = input(
                    "세트를 추가하시겠습니까? (Y/N): "
                ).strip().lower()

                if more not in ("y", "yes", "네", "예"):
                    break

            next_id = max(
                (
                    int(item.get("record_id", 0))
                    for item in workouts
                ),
                default=0
            ) + 1

            record = {
                "record_id": next_id,
                "user_id": user_id,
                "date": date,
                "exercise": exercise,
                "sets": set_list
            }

            workouts.append(record)

            if not self.write_data(user_id, workouts):
                workouts.pop()
                return

            count += 1

            print(f"\n{exercise} 운동 기록 등록 완료!")

            again = input(
                "다른 운동을 등록하시겠습니까? (Y/N): "
            ).strip().lower()

            if again not in ("y", "yes", "네", "예"):
                break

        print(f"\n등록된 운동 종목: {count}개")

    # ==========================================
    # 6. 운동 날짜 및 기록 선택
    # ==========================================

    def select_date(self, workouts, user_id):
        dates = sorted(
            {
                record["date"]
                for record in workouts
                if "date" in record
            },
            reverse=True
        )

        index = self.select_page(
            dates,
            f"{user_id} 운동 날짜 선택"
        )

        if index is None:
            return None

        return dates[index]

    def select_record(self, workouts, date, title):
        date_workouts = [
            record
            for record in workouts
            if record.get("date") == date
        ]

        labels = [
            f"[기록 #{record.get('record_id', '-')}] "
            f"{record.get('exercise', '')}"
            for record in date_workouts
        ]

        index = self.select_page(labels, title)

        if index is None:
            return None

        return date_workouts[index]

    # ==========================================
    # 7. 회원별 운동 기록 조회
    # ==========================================

    def search_workout(self, member):
        print("\n========== 운동 기록 조회 ==========")

        user_id = self.get_user_id(member)
        user_name = self.get_user_name(member)

        print(f"회원 이름: {user_name}")
        print(f"아이디: {user_id}")

        workouts = self.read_data(user_id)

        if workouts is None:
            return

        if not workouts:
            print("등록된 운동 기록이 없습니다.")
            return

        date = self.select_date(workouts, user_id)

        if date is None:
            return

        records = [
            record
            for record in workouts
            if record.get("date") == date
        ]

        print(f"\n========== {date} 운동 기록 ==========")

        for record in records:
            self.print_workout_record(record)

        print(f"\n총 운동 종목: {len(records)}개")

    # ==========================================
    # 8. 운동 기록 수정
    # ==========================================

    def update_workout(self, member):
        print("\n========== 운동 기록 수정 ==========")

        user_id = self.get_user_id(member)
        user_name = self.get_user_name(member)

        print(f"회원 이름: {user_name}")
        print(f"아이디: {user_id}")

        workouts = self.read_data(user_id)

        if workouts is None:
            return

        if not workouts:
            print("수정할 운동 기록이 없습니다.")
            return

        date = self.select_date(workouts, user_id)

        if date is None:
            return

        record = self.select_record(
            workouts,
            date,
            "수정할 운동 종목 선택"
        )

        if record is None:
            return

        self.print_workout_record(record)

        set_list = self.get_set_list(record)

        if not set_list:
            print("수정할 세트가 없습니다.")
            return

        try:
            set_number = int(
                input("수정할 세트 번호 (0: 취소): ")
            )

        except ValueError:
            print("숫자만 입력해주세요.")
            return

        if set_number == 0:
            return

        if not 1 <= set_number <= len(set_list):
            print("존재하지 않는 세트 번호입니다.")
            return

        try:
            weight = float(input("새로운 무게(kg): "))
            reps = int(input("새로운 반복 횟수: "))

        except ValueError:
            print("숫자만 입력해주세요.")
            return

        if weight < 0 or reps <= 0:
            print("무게는 0 이상, 횟수는 1 이상이어야 합니다.")
            return

        # 수정 전 데이터 백업
        original_record = record.copy()

        new_set_list = [
            item.copy()
            for item in set_list
        ]

        new_set_list[set_number - 1]["weight"] = weight
        new_set_list[set_number - 1]["reps"] = reps

        record["sets"] = new_set_list
        record.pop("weight", None)
        record.pop("reps", None)

        if not self.write_data(user_id, workouts):
            record.clear()
            record.update(original_record)
            return

        print("\n운동 기록 수정 완료!")
        self.print_workout_record(record)

    # ==========================================
    # 9. 운동 기록 삭제
    # ==========================================

    def delete_workout(self, member):
        print("\n========== 운동 기록 삭제 ==========")

        user_id = self.get_user_id(member)
        user_name = self.get_user_name(member)

        print(f"회원 이름: {user_name}")
        print(f"아이디: {user_id}")

        workouts = self.read_data(user_id)

        if workouts is None:
            return

        if not workouts:
            print("삭제할 운동 기록이 없습니다.")
            return

        date = self.select_date(workouts, user_id)

        if date is None:
            return

        record = self.select_record(
            workouts,
            date,
            "삭제할 운동 종목 선택"
        )

        if record is None:
            return

        self.print_workout_record(record)

        confirm = input(
            "정말 삭제하시겠습니까? (Y/N): "
        ).strip().lower()

        if confirm not in ("y", "yes", "네", "예"):
            print("삭제를 취소했습니다.")
            return

        index = workouts.index(record)
        workouts.pop(index)

        if not self.write_data(user_id, workouts):
            workouts.insert(index, record)
            return

        print("운동 기록 삭제 완료!")

    # ==========================================
    # 10. 전체 운동 기록 조회
    # ==========================================

    def show_workouts(self):
        print("\n========== 전체 운동 기록 조회 ==========")

        if not self.member_dir.exists():
            print("등록된 운동 기록이 없습니다.")
            return

        users = []

        for folder in sorted(self.member_dir.iterdir()):
            if not folder.is_dir():
                continue

            if not (folder / "workouts.json").exists():
                continue

            workouts = self.read_data(folder.name)

            if workouts:
                users.append(folder.name)

        if not users:
            print("등록된 운동 기록이 없습니다.")
            return

        index = self.select_page(
            users,
            "운동 기록이 있는 회원 선택"
        )

        if index is None:
            return

        user_id = users[index]
        workouts = self.read_data(user_id)

        if not workouts:
            return

        date = self.select_date(workouts, user_id)

        if date is None:
            return

        records = [
            record
            for record in workouts
            if record.get("date") == date
        ]

        print(f"\n========== {user_id} / {date} ==========")

        for record in records:
            self.print_workout_record(record)

        print(f"\n총 운동 종목: {len(records)}개")



# ==========================================
# 실제 회원 정보 불러오기
# ==========================================

def load_members(member_path):
    if not member_path.exists():
        print(f"회원 정보 파일이 없습니다: {member_path}")
        return None

    try:
        with open(member_path, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        print(f"회원 정보 읽기 오류: {error}")
        return None

    # 회원 목록이 리스트인 경우
    if isinstance(data, list):
        members = data

    # 회원 목록이 딕셔너리 안에 있는 경우
    elif isinstance(data, dict):
        members = data.get("members", data.get("회원목록", []))

    else:
        print("회원 정보 형식이 올바르지 않습니다.")
        return None

    if not isinstance(members, list):
        print("회원 목록이 리스트 형식이 아닙니다.")
        return None

    valid_members = []

    for member in members:
        if not isinstance(member, dict):
            continue

        user_id = member.get("아이디") or member.get("user_id")
        name = member.get("이름") or member.get("name")

        if user_id and name:
            valid_members.append({
                **member,
                "아이디": user_id,
                "이름": name
            })

    return valid_members


# ==========================================
# 기능 실행 시 회원 선택
# ==========================================

def select_member(workout, member_path):
    members = load_members(member_path)

    if members is None:
        return None

    if not members:
        print("등록된 회원이 없습니다.")
        return None

    labels = [
        f"{member['이름']} ({member['아이디']})"
        for member in members
    ]

    index = workout.select_page(
        labels,
        "회원 선택"
    )

    if index is None:
        return None

    return members[index]


# ==========================================
# 운동 기록 관리 메뉴
# ==========================================

def workout_menu(workout, member_path):
    while True:
        print("\n========== TMS ==========")
        print("       운동 기록 관리")
        print("=============================")
        print("1. 운동 기록 등록")
        print("2. 운동 기록 조회")
        print("3. 운동 기록 수정")
        print("4. 운동 기록 삭제")
        print("5. 전체 운동 기록 조회")
        print("0. 종료")
        print("=============================")

        choice = input("메뉴 선택: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            return

        elif choice in ("1", "2", "3", "4"):
            # 기능을 선택한 경우에만 회원 선택
            member = select_member(workout, member_path)

            if member is None:
                continue

            if choice == "1":
                workout.register_workout(member)

            elif choice == "2":
                workout.search_workout(member)

            elif choice == "3":
                workout.update_workout(member)

            elif choice == "4":
                workout.delete_workout(member)

        elif choice == "5":
            # 전체 조회는 회원 선택 없이 실행
            workout.show_workouts()

        else:
            print("올바른 메뉴 번호를 입력해주세요.")


# ==========================================
# 프로그램 시작
# ==========================================

def main():
    base_dir = Path(__file__).resolve().parent

    # 프로젝트 최상위 또는 applications 폴더 지원
    if (base_dir / "data").is_dir():
        project_dir = base_dir
    else:
        project_dir = base_dir.parent

    data_dir = project_dir / "data"
    member_dir = data_dir / "members"
    member_path = data_dir / "members.json"

    workout = WorkoutCRUD(member_dir)

    # 실행 즉시 운동 기록 관리 메뉴 출력
    workout_menu(workout, member_path)


if __name__ == "__main__":
    main()
