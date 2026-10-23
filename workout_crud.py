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

    def save_workouts(self):
        self.workout_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.workout_path, "w", encoding="utf-8") as file:
            json.dump(self.workouts, file, ensure_ascii=False, indent=4)

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

    def show_workouts(self):
        print("\n===== 전체 운동 기록 조회=====")
        if not self.workouts:
            print("등록된 운동 기록이 없습니다.")
            return

        for record in self.workouts:
            print(f"기록 번호:{record['record_id']}")
            print(f"회원 ID: {record['user_id']}")
            print(f"운동 날짜:{record['date']}")
            print(f"운동 종목:{record['exercise']}")
            print(f"운동 무게:{record['weight']}kg")
            print(f"반복 횟수:{record['reps']}회")
            print(f"세트 수:{record['sets']}세트")    
            print("-"*30)        
        
        print(f'전체 운동 기록 수 : {len(self.workouts)}개')

    def register_workout(self):
        print("===== 운동 기록 등록 =====")

        user_id = input("회원 ID: ").strip()
        date = input("운동 날짜(YYYY-MM-DD): ").strip()

        exercise = self.select_exercise()

        if exercise is None:
            print("운동 기록 등록을 취소합니다.")
            return
        
        try:
            weight = float(input("운동 무게(kg): "))
            reps = int(input("반복 횟수: "))
            sets = int(input("세트 수: "))

        except ValueError:
            print("숫자만 입력해주세요.")
            return

        if weight < 0:
            print("운동 무게는 0kg 이상이여야 합니다.")
            return

        if reps <= 0 or sets <= 0:
            print("반복 횟수와 세트 수는 1 이상이여야 합니다.")
            return

        next_id = max((record["record_id"] for record in self.workouts), default=0) + 1
    
        record = {
            "record_id": next_id,
            "user_id": user_id,
            "date": date,
            "exercise": exercise,
            "weight": weight,
            "reps": reps,
            "sets": sets,
        }

        self.workouts.append(record)

        self.save_workouts()

        print("운동 기록 등록 완료!")

    def search_workout(self):
        print("\n===== 회원별 운동 기록 조회 =====")

        user_id = input("조회할 회원 ID: ").strip()
        count = 0

        for record in self.workouts:
            if record["user_id"] == user_id:
                count += 1
                print(f"\n[운동 기록 {count}]")
                print(f"기록 번호:{record['record_id']}")
                print(f"운동 날짜:{record['date']}")
                print(f"운동 종목:{record['exercise']}")
                print(f"운동 무게:{record['weight']}kg")
                print(f"반복 횟수:{record['reps']}회")
                print(f"세트 수:{record['sets']}세트")

        if count == 0:
            print("해당 회원의 운동 기록이 없습니다.")

    def update_workout(self):
        print("\n===== 운동 기록 수정 =====")

        try:
            record_id = int(input("수정할 기록 번호: "))
        except ValueError:
            print("기록 번호는 숫자로 입력해주세요.")
            return

        for record in self.workouts:
            if record["record_id"] == record_id:
                print(f"운동 종목:{record['exercise']}")
                print(f"운동 무게:{record['weight']}kg")
                print(f"반복 횟수:{record['reps']}회")
                print(f"세트 수:{record['sets']}세트")

                new_exercise = input("새로운 운동 종목: ").strip()

                if not new_exercise:
                    print("운동 종목은 비워둘 수 없습니다.")
                    return

                try:
                    new_weight = float(input("새로운 운동 무게(kg): "))
                    new_reps = int(input("새로운 반복 횟수: "))
                    new_sets = int(input("새로운 세트 수: "))
                except ValueError:
                    print("무게, 반복 횟수, 세트 수는 숫자로 입력해주세요.")
                    return
                if new_weight < 0:
                    print("운동 무게는 0kg 이상이어야 합니다.")
                    return
                if new_reps <= 0 or new_sets <= 0:
                    print("반복 횟수와 세트 수는 1 이상어이야 합니다.")
                    return

                record["exercise"] = new_exercise
                record["weight"] = new_weight
                record["reps"] = new_reps
                record["sets"] = new_sets

                self.save_workouts()

                print("운동 기록 수정 완료!")
                return

        print("해당 기록 번호를 찾을 수 없습니다.")

    def delete_workout(self):
        print("\n===== 운동 기록 삭제 =====")

        try:
            record_id = int(input("삭제할 기록 번호: "))
        except ValueError:
            print("기록 번호는 숫자로 입력해 주세요.")
            return

        for record in self.workouts:
            if record.get("record_id") == record_id:
                print(f"운동 종목: {record['exercise']}")
                print(f"운동 무게: {record['weight']}kg")
                print(f"운동 횟수: {record['reps']}회")
                print(f"세트 수: {record['sets']}세트")

                confirm = input("정말 삭제하시겠습니까? (y/n): ").strip().lower()

                if confirm != "y":
                    print("운동 기록 삭제를 취소했습니다.")
                    return

                self.workouts.remove(record)
                self.save_workouts()

                print("운동 기록 삭제 완료!")
                return

        print("해당 기록 번호를 찾을 수 없습니다.")

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
