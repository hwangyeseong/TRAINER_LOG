import json
from pathlib import Path


class WorkoutCRUD:
    def __init__(self, workout_path):
        self.workout_path = Path(workout_path)

        if self.workout_path.exists():
            with open(self.workout_path, "r", encoding="utf-8") as file:
                self.workouts = json.load(file)
        else:
            self.workouts = []

    # 목록을 10개씩 보여주고 선택하는 공통 함수
    def select_page(self, items, title, page_size=10):

        if not items:
            print("선택할 항목이 없습니다.")
            return None

        page = 0
        max_page = (len(items) - 1) // page_size

        while True:
            start = page * page_size
            end = start + page_size
            page_list = items[start:end]

            print(f"\n===== {title} =====")
            print(f"페이지 {page + 1} / {max_page + 1}")

            # 현재 페이지 목록 출력
            for index, item in enumerate(page_list, start=start + 1):
                print(f"{index}. {item}")

            print("\n< 이전 페이지 | > 다음 페이지 | 0 취소")

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
                print("선택을 취소했습니다.")
                return None

            elif choice.isdigit():
                number = int(choice)

                if 1 <= number <= len(items):
                    return items[number - 1]

                print("목록에 있는 번호를 선택해주세요.")

            else:
                print("올바른 번호를 입력해주세요.")

    def save_workouts(self):
        self.workout_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.workout_path, "w", encoding="utf-8") as file:
            json.dump(self.workouts, file, ensure_ascii=False, indent=4)

    def print_workout_record(self, record):
        print("\n" + "=" * 54)
        print(f" [기록 #{record['record_id']}] {record['exercise']}")
        print(f" 회원 ID : {record['user_id']}")
        print(f" 운동 날짜 : {record['date']}")
        print("-"* 54)

        print(f"{'세트' :<8}{'무게':<12}{'횟수':<10}{'볼륨'}")
        print("-"*54)

        total_volume = 0

        if isinstance(record["sets"], list):
            for set_record in record["sets"]:
                set_num = set_record["set"]
                weight = set_record["weight"]
                reps = set_record["reps"]
                volume = weight * reps

                total_volume += volume

                print(
                    f"{set_num:<8}"
                    f"{str(weight) + 'kg':<12}"
                    f"{str(reps) + '회':<10}"
                    f"{volume:,.1f}kg"
                )
            total_sets = len(record["sets"])

        else:
            weight = record["weight"]
            reps = record["reps"]
            total_sets = record["sets"]
            total_volume = weight * reps * total_sets

            for set_num in range(1, total_sets + 1):
                print(
                    f"{set_num:<8}"
                    f"{str(weight) + 'kg':<12}"
                    f"{str(reps) + '회':<10}"
                    f"{weight * reps:,.1f}kg"
                )
        print("-"* 54)
        print(
            f"총 {total_sets}세트 | "
            f"총 볼륨: {total_volume:.1f}kg"
        )
        print("="*54)

    def select_exercise(self):
        machine_path = self.workout_path.parent / "muscles.json"

        if not machine_path.exists():
            print("운동 종목 파일이 없습니다.")
            return None

        with open(machine_path, "r", encoding="utf-8") as file:
            body_list = json.load(file)

        # 운동 부위 5가지
        muscle_list = ["Core", "Back", "Chest", "Shoulders", "Arms", "Legs"]

        print("\n===== 운동 부위 선택 =====")

        for index, muscle in enumerate(muscle_list, start =1):
            print(f"{index}. {muscle}")

        print("0. 취소")

        while True:
            choice = input("운동 부위 번호 선택").strip()

            if choice == "0":
                return None
            if not choice.isdigit():
                print("숫자만 입력해주세요.")
                continue
            number = int(choice)

            if 1 <= number <= len(muscle_list):
                selected_muscle = muscle_list[number -1]
                break

            print("목록에 있는 번호를 선택해주세요.")

        # 선택한 운동 부위의 세부 운동 찾기
        exercise_list = []

        for body in body_list:
            if body["muscle"] == selected_muscle:
                exercise_list.extend(body["machines"])

        if not exercise_list:
            print(f"{selected_muscle}에 등록된 운동이 없습니다.")
            return None

        print(f"\n===== {selected_muscle} 운동 종목 선택 =====")

        for index, exercise in enumerate(exercise_list, start =1):
            print(f'{index}. {exercise}')

        print("0 취소")

        while True:
            choice = input("운동 번호 선택 (0: 취소): ").strip()

            if choice == "0":
                return None

            if not choice.isdigit():
                print("숫자만 입력해주세요.")
                continue
            
            number = int(choice)

            if 1 <= number <= len(exercise_list):
                exercise =exercise_list[number - 1]
                print(f'선택한 운동: {exercise}')
                return exercise
        
            print("목록에 있는 번호를 선택해주세요.")

        # 전체 운동 기록 조회
    def show_workouts(self):
        print("\n===== 전체 운동 기록 조회 =====")

        # 1. 운동 기록 존재 여부 확인
        if not self.workouts:
            print("등록된 운동 기록이 없습니다.")
            return

        # 2. 운동 기록에 등록된 회원 ID 목록 생성
        user_list = sorted({
            record["user_id"]
            for record in self.workouts
        })

        # 3. 회원 선택 (10개씩 페이지 표시)
        selected_user = self.select_page(
            user_list,
            "운동 기록이 있는 회원 목록"
        )

        if selected_user is None:
            return

        # 4. 선택한 회원의 운동 기록 찾기
        user_workouts = [
            record for record in self.workouts
            if record["user_id"] == selected_user
        ]

        # 5. 운동 날짜 목록 생성 (최신순)
        date_list = sorted(
            {record["date"] for record in user_workouts},
            reverse=True
        )

        # 6. 날짜 선택 (10개씩 페이지 표시)
        selected_date = self.select_page(
            date_list,
            f"{selected_user} 회원의 운동 날짜 선택"
        )

        if selected_date is None:
            return

        # 7. 선택한 날짜의 운동 기록 찾기
        date_workouts = [
            record for record in user_workouts
            if record["date"] == selected_date
        ]

        # 8. 해당 날짜의 운동 기록 출력
        print(
            f"\n===== {selected_user} / "
            f"{selected_date} 운동 기록 ====="
        )

        for record in date_workouts:
            self.print_workout_record(record)

        # 9. 조회 결과 요약
        print(f"\n회원 ID: {selected_user}")
        print(f"운동 날짜: {selected_date}")
        print(f"운동 종목 수: {len(date_workouts)}개")

    
    def register_workout(self):
        print("\n===== 운동 기록 등록 =====")

        # 회원 ID와 날짜는 처음 한 번만 입력
        user_id = input("회원 ID: ").strip()
        date = input("운동 날짜(YYYY-MM-DD): ").strip()

        if not user_id or not date:
            print("회원 ID와 날짜는 비워둘 수 없습니다.")
            return

        count = 0

        # 운동을 여러 개 등록하기 위한 반복문
        while True:
            exercise = self.select_exercise()

            if exercise is None:
                print("운동 선택을 취소했습니다.")
                break

            print(f"\n===== {exercise} 세트 기록 =====")

            set_list = []

            while True:
                set_number = len(set_list) + 1

                print(f"\n--- {set_number}세트 ---")

                try:
                    weight = float(input("운동 무게(kg): "))
                    reps = int(input("반복 횟수: "))
                except ValueError:
                    print("숫자만 입력해주세요.")
                    continue
                    
                if weight < 0 or reps <= 0:
                    print("무게는 0 이상, 반복 횟수는 1 이상이어야 합니다.")
                    continue

                set_record = {
                    "set": set_number,
                    "weight": weight,
                    "reps": reps
                }

                set_list.append(set_record)

                while True:
                    more_sets = input("세트를 추가하시겠습니까? (Y/N) ").strip().lower()

                    if more_sets in ("y", "n"):
                        break

                    print("Y 또는 N을 입력해주세요.")

                if more_sets == "n":
                    break
            
            next_id = max(
                (record["record_id"] for record in self.workouts),
                default=0
            ) + 1

            record = {
                "record_id": next_id,
                "user_id": user_id,
                "date": date,
                "exercise": exercise,
                "sets": set_list
            }

            self.workouts.append(record)
            self.save_workouts()

            count += 1

            print(f"\n{exercise} 운동 기록 등록 완료!")

            # 다른 운동을 추가할지 확인
            while True:
                again = input(
                    "\n다른 운동을 추가하시겠습니까? (Y/N): "
                ).strip().lower()

                if again in ("y", "n"):
                    break

                print("Y 또는 N을 입력해주세요.")

            if again == "n":
                break

        print("\n===== 운동 기록 등록 종료 =====")
        print(f"이번에 등록한 운동 종목: {count}개")

    # 회원별 운동 기록 조회
    def search_workout(self):
        print("\n===== 회원별 운동 기록 조회 =====")

        # 1. 회원 ID 입력
        user_id = input("조회할 회원 ID: ").strip()

        # 2. 해당 회원의 운동 기록만 가져오기
        user_workouts = [
            record for record in self.workouts
            if record["user_id"] == user_id
        ]

        if not user_workouts:
            print("해당 회원의 운동 기록이 없습니다.")
            return

        # 3. 운동한 날짜 목록 만들기 (중복 제거)
        date_list = sorted(
            {record["date"] for record in user_workouts},
            reverse=True
        )

        # 4. 날짜 선택 (10개씩 페이지 표시)
        selected_date = self.select_page(
            date_list,
            f"{user_id} 회원의 운동 날짜 선택"
        )

        if selected_date is None:
            return

        # 5. 선택한 날짜의 운동 기록 가져오기
        date_workouts = [
            record for record in user_workouts
            if record["date"] == selected_date
        ]

        # 6. 해당 날짜의 운동 기록 출력
        print(f"\n===== {selected_date} 운동 기록 =====")

        for record in date_workouts:
            self.print_workout_record(record)

        print(f"\n총 운동 종목: {len(date_workouts)}개")

        print(f"\n총 운동 종목: {len(date_workouts)}개")

       # 운동 기록 수정
    def update_workout(self):
        print("\n===== 운동 기록 수정 =====")

        # 1. 회원 ID 입력
        user_id = input("수정할 회원 ID: ").strip()

        # 2. 해당 회원의 운동 기록 찾기
        user_workouts = [
            record for record in self.workouts
            if record["user_id"] == user_id
        ]

        if not user_workouts:
            print("해당 회원의 운동 기록이 없습니다.")
            return

        # 3. 운동 날짜 목록 만들기
        date_list = sorted(
            {record["date"] for record in user_workouts},
            reverse=True
        )

        # 4. 운동 날짜 선택
        selected_date = self.select_page(
            date_list,
            f"{user_id} 회원의 운동 날짜 선택"
        )

        if selected_date is None:
            return

        # 5. 선택한 날짜의 운동 기록 찾기
        date_workouts = [
            record for record in user_workouts
            if record["date"] == selected_date
        ]

        # 6. 운동 종목 선택용 목록 만들기
        exercise_list = [
            f"[기록 #{record['record_id']}] {record['exercise']}"
            for record in date_workouts
        ]

        selected_exercise = self.select_page(
            exercise_list,
            f"{selected_date} 운동 종목 선택"
        )

        if selected_exercise is None:
            return

        # 7. 선택한 운동 기록 가져오기
        selected_index = exercise_list.index(selected_exercise)
        record = date_workouts[selected_index]

        print("\n===== 수정 전 운동 기록 =====")
        self.print_workout_record(record)

        # 8. 기존 데이터도 세트별 구조로 변환
        if isinstance(record["sets"], list):
            set_list = record["sets"]
        else:
            set_list = []

            for i in range(1, record["sets"] + 1):
                set_list.append({
                    "set": i,
                    "weight": record["weight"],
                    "reps": record["reps"]
                })

        # 9. 수정할 세트 선택
        try:
            set_number = int(
                input("\n수정할 세트 번호 (0: 취소): ")
            )
        except ValueError:
            print("숫자만 입력해주세요.")
            return

        if set_number == 0:
            print("운동 기록 수정을 취소했습니다.")
            return

        if not 1 <= set_number <= len(set_list):
            print("존재하지 않는 세트 번호입니다.")
            return

        # 10. 새로운 무게와 횟수 입력
        try:
            new_weight = float(
                input("새로운 운동 무게(kg): ")
            )

            new_reps = int(
                input("새로운 반복 횟수: ")
            )

        except ValueError:
            print("숫자만 입력해주세요.")
            return

        if new_weight < 0 or new_reps <= 0:
            print("무게는 0 이상, 횟수는 1 이상이어야 합니다.")
            return

        # 11. 선택한 세트 수정
        set_list[set_number - 1]["weight"] = new_weight
        set_list[set_number - 1]["reps"] = new_reps

        # 12. 수정된 데이터를 기록에 반영
        record["sets"] = set_list

        # 이전 데이터 구조의 중복 항목 제거
        record.pop("weight", None)
        record.pop("reps", None)

        # 13. JSON 파일에 저장
        self.save_workouts()

        print("\n===== 운동 기록 수정 완료 =====")
        self.print_workout_record(record)
                     

        # 운동 기록 삭제
    def delete_workout(self):
        print("\n===== 운동 기록 삭제 =====")

        # 1. 회원 ID 입력
        user_id = input("삭제할 회원 ID: ").strip()

        # 2. 해당 회원의 운동 기록 찾기
        user_workouts = [
            record for record in self.workouts
            if record["user_id"] == user_id
        ]

        if not user_workouts:
            print("해당 회원의 운동 기록이 없습니다.")
            return

        # 3. 운동 날짜 목록 만들기 (최신 날짜순)
        date_list = sorted(
            {record["date"] for record in user_workouts},
            reverse=True
        )

        # 4. 운동 날짜 선택
        selected_date = self.select_page(
            date_list,
            f"{user_id} 회원의 운동 날짜 선택"
        )

        if selected_date is None:
            print("운동 기록 삭제를 취소했습니다.")
            return

        # 5. 선택한 날짜의 운동 기록 찾기
        date_workouts = [
            record for record in user_workouts
            if record["date"] == selected_date
        ]

        # 6. 운동 종목 목록 만들기
        exercise_list = [
            f"[기록 #{record['record_id']}] {record['exercise']}"
            for record in date_workouts
        ]

        # 7. 삭제할 운동 종목 선택
        selected_exercise = self.select_page(
            exercise_list,
            f"{selected_date} 삭제할 운동 종목 선택"
        )

        if selected_exercise is None:
            print("운동 기록 삭제를 취소했습니다.")
            return

        # 8. 선택한 운동 기록 가져오기
        selected_index = exercise_list.index(selected_exercise)
        record = date_workouts[selected_index]

        # 9. 삭제할 기록 상세정보 출력
        print("\n===== 삭제할 운동 기록 =====")
        self.print_workout_record(record)

        # 10. 삭제 여부 확인
        confirm = input(
            "\n정말 삭제하시겠습니까? (Y/N): "
        ).strip().lower()

        if confirm != "y":
            print("운동 기록 삭제를 취소했습니다.")
            return

        # 11. 선택한 기록만 삭제
        self.workouts.remove(record)

        # 12. JSON 파일에 저장
        self.save_workouts()

        print("\n운동 기록 삭제 완료!")


def workout_menu(workout):
    while True:
        print("\n========== 운동 기록 관리 ==========")
        print("1. 운동 기록 등록")
        print("2. 회원별 운동 기록 조회")
        print("3. 운동 기록 수정")
        print("4. 운동 기록 삭제")
        print("5. 전체 운동 기록 조회")
        print("0. 이전 메뉴")
        print("====================================")

        choice = input("메뉴 선택: ").strip()

        if choice == "1":
            workout.register_workout()
        elif choice == "2":
            workout.search_workout()
        elif choice == "3":
            workout.update_workout()
        elif choice == "4":
            workout.delete_workout()
        elif choice == "5":
            workout.show_workouts()
        elif choice == "0":
            print("운동 기록 관리를 종료합니다.")
            break    
        else:
            print("올바른 메뉴 번호를 입력해주세요.")



if __name__ == "__main__":
    workout_path = Path(__file__).resolve().parent / "data" / "workouts.json"
    workout = WorkoutCRUD(workout_path)

    workout_menu(workout)

