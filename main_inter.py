import os.path

from before_func_inter import before_func

if __name__ == '__main__':
    # 이전 데이터가 없으면 조건 추가
    uid = input("uid 를 입력하세요.\n")
    folder = "Data/"
    file = folder + uid + ".txt"
    
    before_func(uid)
