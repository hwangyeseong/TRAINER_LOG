import os
import json
from datetime import datetime

class TrainerCRUD:
    def __init__(self, member_path):
        self.member_path = member_path
        with open(self.member_path, "r", encoding='utf-8') as f:
            self.members = json.load(f)  # load members.json
        
    def do_save(self):
        # today = datetime.now().strftime("%y%m%d")
        today = datetime.now().strftime("%y/%m/%d %H:%M:%S")
        # # 이미 멤버가 존재할 때
        # if self.members:
        #     ymd = self.members[-1]['save_time']
        #     if ymd[:6] == str(datetime.now().strftime("%y%m%d")):
        #         count = int(ymd[6:]) + 1
        #     else:
        #         count = 0
        # # 최초 기록
        # else:
        #     count = 0
            
        # if count>999:
        #     print("하루 최대 등록 인원을 초과했습니다.")
        #     return False
        
        #이름, 이메일의 작성양식 추가 필요
        user_id = input("아이디를 입력하세요: ")
        name = input("이름을 입력하세요: ")
        email = input("이메일을 입력하세요: ")
        save_time = str(today)
        modify_time = str(today)
        # save_time = str(today)+f'{count:03d}' # 등록일
        
        #일단은 중복된 존재가 없다는 가정하에 모두 중복처리를 해놨고
        #만약 동명이인에 대한 논의가 끝나면 수정필요
        for member in self.members:
            if (member['user_id'] == user_id):
                print("이미 존재하는 멤버입니다.")
                return False
            elif (member['name'] == name):
                print("이미 존재하는 이름입니다.")
                return False
            elif (member['email'] == email):
                print("이미 존재하는 이메일입니다.")
                return False
        
        new_member = {'user_id': user_id,
                      'name': name,
                      'email': email,
                      'save_time': save_time,
                      'modify_time': modify_time}
        
        # 전체 멤버 데이터베이스에 새 멤버 등록
        self.members.append(new_member)
        with open(self.member_path, mode='w', encoding='utf-8') as f:
            json.dump(self.members, f, ensure_ascii=False, indent=4)
            
        print(f"{user_id}: {name} 등록에 성공했습니다.")
        
        return True
    
    def do_retrive(self):
        if self.members:
            # #1줄보기
            # print("=======전체 회원 리스트=======")
            # for index, member in enumerate(self.members.copy()):
            #     print(f"ㅡㅡㅡㅡㅡㅡㅡNo.{index + 1:03d}ㅡㅡㅡㅡㅡㅡㅡ")
            #     for key, value in member.items():
            #         print(f"{key:<8}: {value:^10}")
            # print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
            
            ## 2줄보기
            print(f"{"=======전체 회원 리스트=======":^77}")
            for index, member in enumerate(self.members):
                if (index % 2) == 0:
                    a=[(key,value) for key, value in member.items()]
                    if index == (len(self.members)-1):
                        print(f'+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index+1}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index+2}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+')
                        for i in range(len(a)):
                            print(f"| {a[i][0]:<13}: {a[i][1]:^25} | {" ":<13}: {" ":^25} |")    
                else:
                    b=[(key,value) for key, value in member.items()]
                    print(f'+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡNo.{index+1}ㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+')
                    for i in range(len(a)):
                        print(f"| {a[i][0]:<13}: {a[i][1]:^25} | {b[i][0]:<13}: {b[i][1]:^25} |")
            print('+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+-ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ-+')
            return True
        else:
            print("등록된 회원이 없습니다.")
            return False
            
    def do_select_one(self, select_num="1"):
        if self.members:
            word = {"1":"조회", "3":"수정", "4":"삭제"}[select_num]
            select_member = input(f"{word} 할 회원 이름을 입력해주세요: ")
            count=0 #동명이인 관리할때 count=1로 만들면 바로 관리가능
            detail_member=[]
            
            for member in self.members:
                if select_member == member['name']:
                    count += 1
                    detail_member.append(member)
                    
            if count == 0:
                print("존재하지 않는 회원입니다.")
                return False
            
            elif count == 1:
                print("ㅡ" * 20)
                for key, value in detail_member[0].items():
                    print(f"{key:<12}: {value:^10}")
                print("ㅡ" * 20)
                
                if select_num == "1": #전체조회"2"->개인검색"1"
                    return detail_member[0]
                
                elif select_num == "3": #정보수정"3"
                    is_modify = input("수정하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower()
                                
                    if is_modify in ("y", "yes", "예", "네"):
                        self.modify_member(detail_member[0])
                        
                        with open(self.member_path, mode='w', encoding='utf-8') as f:
                            json.dump(self.members, f, ensure_ascii=False, indent=4)
                        
                        return True
                    else:
                        print("이전으로 돌아갑니다.")
                        return False
                    
                elif select_num == "4": #정보삭제"4"
                    is_delete = input("삭제하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower()
                                
                    if is_delete in ("y", "yes", "예", "네"):
                        self.members.remove(detail_member[0])
                        
                        with open(self.member_path, mode='w', encoding='utf-8') as f:
                            json.dump(self.members, f, ensure_ascii=False, indent=4)
                        print("회원 삭제에 성공했습니다.")
                        return True
                    else:
                        print("이전으로 돌아갑니다.")
                        return False
                    
            else:
                print("동명이인이 존재합니다.")
                print("=======동명이인 리스트=======")
                for  i, m in enumerate(detail_member):
                    print(f"ㅡㅡㅡㅡㅡㅡㅡNo.{i + 1:03d}ㅡㅡㅡㅡㅡㅡㅡ")
                    for key, value in m.items():
                        print(f"{key:<10}: {value:^10}")
                print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ")
                same_num = input("조회할 번호를 선택하세요: ")
                
                print("ㅡ" * 10)
                for key, value in detail_member[0].items():
                    print(f"{key:<10}: {value:^10}")
                print("ㅡ" * 10)
                
                if select_num == "1": #전체조회"2"->개인검색"1"
                    return detail_member[int(same_num)-1]
                
                elif select_num == "3": #정보수정"3"
                    is_modify = input("수정하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower()
                    if is_modify in ("y", "yes", "예", "네"):
                        self.modify_member(detail_member[int(same_num)-1])
                        
                        with open(self.member_path, mode='w', encoding='utf-8') as f:
                            json.dump(self.members, f, ensure_ascii=False, indent=4)
                        
                        return True
                    else:
                        print("이전으로 돌아갑니다.")
                        return False
                    
                elif select_num == "4": #정보삭제"4"
                    is_delete = input("삭제하실 정보가 다음 정보가 맞습니까?(Y/N): ").strip().lower()
                    if is_delete in ("y", "yes", "예", "네"):
                        self.members.remove(detail_member[int(same_num)-1])
                        
                        with open(self.member_path, mode='w', encoding='utf-8') as f:
                            json.dump(self.members, f, ensure_ascii=False, indent=4)
                        print("회원 삭제에 성공했습니다.")
                        return True
                    else:
                        print("이전으로 돌아갑니다.")
                        return False
        else:
            print("등록된 회원이 없습니다.")
            return False
        
    def modify_member(self, select_member):
        print("회원 정보 수정을 시작합니다.\n")
        option = [key for key, _ in select_member.items()]
        while True:
            modify_key = input("수정할 정보를 선택해주세요?[name, email, ...]: ")
            if modify_key in option:
                for member in self.members:
                    if member == select_member:
                        for key, value in member.items():
                            if key == modify_key:
                                modify_value=input(f"기존 {key}는 {value}입니다. 변경할 내용을 적어주세요: ")
                                is_modify = input(f"정말 {modify_value}로 변경하시겠습니까?(Y/N): ").strip().lower()
                                if is_modify in ("y", "yes", "예", "네"):
                                    member[key]=modify_value
                                    member['modify_time'] = datetime.now().strftime("%y/%m/%d %H:%M:%S")
                                    print(f"{modify_key} 변경에 성공했습니다.")
                                    return True
                                else:
                                    print("\n이전으로 돌아갑니다.\n")
                                    
            else:
                print("잘못된 접근입니다.")
                is_continue = input("계속하시겠습니까?(Y/N): ").strip().lower()
                if is_continue in ("y", "yes", "예", "네"):
                    print("\n")
                else:
                    return
    
    
    
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
    # trainer_interface(train_sys)