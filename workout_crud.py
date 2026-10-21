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

    def show_workouts(self):
        print(self.workouts)

    def register_workout(self):
        print("===== 운동 기록 등록 =====")

        user_id = input("회원 ID: ")
        date = input("운동 날짜(YYYY-MM-DD): ")
        exercise = input("운동 종목: ")
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

        record = {
            "record_id": len(self.workouts) +1,
            "user_id": user_id,
            "date": date,
            "exercise": exercise,
            "weight": weight,
            "reps": reps,
            "sets": sets
        }

        self.workouts.append(record)

        self.workout_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.workout_path, "w", encoding="utf-8") as file:
            json.dump(self.workouts, file, ensure_ascii=False, indent=4)

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

                record["exercise"] = new_exercise

                print("운동 종목 수정 완료!")
                return

                self.workout_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.workout_path, "w", encoding='utf-8') as file:
                    json.dump(self.workout, file, ensure_ascii=False, indent=4)

        print("해당 기록 번호를 찾을 수 없습니다.")

if __name__ =="__main__":
    workout_path = Path(__file__).resolve().parent / "data" / "workouts.json"
    workout = WorkoutCRUD(workout_path)

    workout.update_workout()
    # workout.search_workout()
    # workout.register_workout()
    # workout.show_workouts()
