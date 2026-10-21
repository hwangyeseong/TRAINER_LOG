import os
import json

from trainer_crud import TrainerCRUD

def login_interface():
    # 대부분의 사이트는 id/pw를 한번에 입력해서 실패하면 다시 둘다 입력하게 하는데
    # 유사하게 구현할지 카운트만 같이하고 따로 할지 고민중
    print("========관리자 로그인========")
    login_count = 0
    
    while True:
        login_id = input("관리자id: ").strip()
        login_pw = input("관리자pw: ").strip()
        if login_id != "admin" or login_pw != "0000":
            login_count += 1
            print(f"존재하지 않는 관리자입니다.({login_count}/5회 틀림)")
            if login_count >= 5:
                print("아이디 입력 횟수를 초과하였습니다.\n")
                return
        else:
            print("로그인에 성공했습니다.")
            return True
        
    print("========================")   

def trainer_interface(members):
    while True:        
        print(
            "\n=======회원 관리 모드=======\n"
            "1. 회원 등록\n"
            "2. 전체 회원 조회\n"
            "3. 회원 정보 수정\n"
            "4. 회원 삭제\n"
            "5. 부가 서비스 관리\n"
            "6. 프로그램 종료\n"
            "============================"
            )
        select_num = input("번호를 입력하세요: ").strip()
        print(" ")
        
        if select_num == "1":
            print("1. 회원 등록을 선택하셨습니다.\n")
            members.do_save()
            #중복처리 필요
            # 여기서 작성한 고유번호/이름/이메일을 이용하여 개인폴더 생성
            #그리고 각 폴더에 details/diet/records/requires.json 생성  
                
        elif select_num == "2":
            print("2. 전체 회원 조회를 선택하셨습니다. ")
            if not search_interface(members):
                return False
            
        elif select_num == "3":
            print("3. 회원 정보 수정을 선택하셨습니다.")
            # members.do_modify_one()
            members.do_select_one(select_num)
                        
        elif select_num == "4":
            print("4. 회원 삭제를 선택하셨습니다.")
            # members.do_delete_one()
            members.do_select_one(select_num)
        elif select_num == "5":
            print("5. 부가 서비스 관리를 선택하셨습니다.")
            
        elif select_num == "6":
            print("프로그램을 종료합니다.\n")
            break
        else:
            print("잘못된 접근입니다.\n")
        
def search_interface(members):
    #members.json의 리스트를 가져왔다고 가정
    #리스트를 고유번호, 이름, 이메일만 추출
    # 그냥 리스트 자체를 출력할지, 틀에 맞춰 출력할지 선택
    while True:
        if not members.do_retrive():
            return True
        
        print(
            "\n=======회원 검색 모드=======\n"
            "1. 회원 검색\n"
            "2. 이전으로\n"
            "3. 프로그램 종료\n"
            "============================"
            )
        search_num = input("번호를 선택하세요: ")
        
        if search_num == "1":
            print("1. 회원 검색을 시작합니다.")
            # detail_member = members.do_select_one()
            detail_member = members.do_select_one(search_num)
            
            if detail_member:
                if not detail_interface(detail_member):
                    return False
                
            else:
                pass
            
        elif search_num == "2":
            print("이전 화면으로 돌아갑니다.")
            return True
        
        elif search_num == "3":
            print("프로그램을 종료합니다.")
            return False
        
        else:
            print("잘못된 접근입니다.\n")
        
def detail_interface(member):
    see_more = input(f"{member['name']}님을 조회하시겠습니까?(Y/N): ").strip().lower()
    if see_more in ("y", "yes", "네", "예"):
        
        while True:    
            print(
                f"\n==========={member['name']}===========\n"
                "1. 상세 기록 조회\n"
                "2. 운동 종목 관리\n"
                "3. 운동 기록 관리\n"
                "4. 식단 관리\n"
                "5. \n"
                "6. 이전으로\n"
                "7. 프로그램 종료\n"
                "==========================\n"
                )
            
            detail_num = input("조회할 내용(번호)을 선택해주세요: ").strip()
            if detail_num == "1":
                print("\n1. 상세 기록 조회를 선택하셨습니다.")
                
                for key, value in member.items():
                    print(f"{key:<10}: {value:^10}")
                #지금은 members.json의 내용들만 반환하지만 details.json을 추가함에 따라 변동될 예정
                
            elif detail_num == "2":
                print("\n2. 운동 종목 관리를 선택하셨습니다.")
                
            elif detail_num == "3":
                print("\n3. 운동 기록 관리를 선택하셨습니다.")
                
            elif detail_num == "4":
                print("\n4. 식단 관리를 선택하셨습니다.")
                
            
            elif detail_num == "6":
                print("이전 화면으로 돌아갑니다.")
                return True
            
            elif detail_num == "7":
                print("프로그램을 종료합니다.\n")
                return False
            
            else:
                print("잘못된 접근입니다.\n")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #C:\Users\jihun\Archive\aicon\mini_project
    DATA_DIR = os.path.join(BASE_DIR, 'data') #C:\Users\jihun\Archive\aicon\mini_project\data
    member_path = os.path.join(DATA_DIR, 'members.json')
    # train_sys = TrainerCRUD(member_path)
    with open(member_path, "r", encoding='utf-8') as f:
                members = json.load(f)
    # if login_interface():
    #     trainer_interface(members)
    train_sys = TrainerCRUD(member_path)
    trainer_interface(train_sys)
            
            
            
'''
===============================================================================
~2026.10.16
트레이너 앱
트레이너 로그인

=======GYM LOG=======
1. 회원 등록 및 관리
2. 운동 종목 관리
3. 회원별 운동 기록 등록
4. 회원별 운동 기록 조회
5. 프로그램 종료

메뉴를 선택하세요:4
회원 ID 입력: user01

[김철수 회원 운동 기록]
10/12|벤치프레스|40kg|10회|3세트
10/13|스쿼트|60kg|12회|3세트

회원 관리CRUD: 등록, 조회, 수정, 삭제 ->필수
운동 종목 관리CRUD: 운동 종목 등록, 조회, 수정, 삭제 -> 필수
개인별 운동 기록: 회원별 운동 날짜, 무게, 횟수, 세트 기록 및 조회->핵심추가기능
데이터 저장: JSON 파일 저장 및 불러오기 ->필수
운동 기록 통계: 운동별 기록 변화 확인 ->선택

데스크 직원: 회원등록조회/회원복 및 락커 이용 기간 확인
트레이너: 회원별 운동 기록 등록 조회/운동 종목 관리

-외부 API 및 크롤링: 회원 인바디에 따른 섭취 음식 칼로리 계산(식품안전나라에서 '식품 영양성분 데이터베이스'를 오픈API 형태로 무상 제공)

'''
'''
=================================================================
2026.10.17
코딩을 하려고 보니까 회원리스트를 먼저 내보내면 선택화면이 가려질 우려가 있어서 뒤로 옮기고
"전체 멤버 조회" -> "회원 검색" -> "개별 데이터 조회" 시스템으로 구성
관계도도 TrainerCRUD2.png로 수정

이거에 맞게 login_interface(), trainer_interface(), search_interface(), detail_interface() 작성
login_interface(): 로그인 화면
trainer_interface(): 회원관리CRUD
search_interface(): 검색 화면
detail_interface(): 개인관리 CRUD

일단 내용은 텍스트로 대체

주요 의논점
1. 중복처리 기준 마련(이름, 이메일로 끝낼건지, 전화번호도 추가할건지 아니면 다른 기준이 있는지)
2. 전체적인 구조에 조금 디테일이 필요해보임
3. 개인관리 CRUD에 해당하는 데이터들의 관리 형식(개인별 폴더 or 주제별 파일)
4. 전체 회원 조회 출력방식(정제된 데이터 OR lIST그대로)

'''
#if elif 로 번호를 쓴 것들 match-case로 바꿔도됨