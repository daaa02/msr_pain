import os.path

from before_func import before_func
from after_func import after_func

from NLP import NLP, Dictionary

from QLearning.QL_algorithm_before import Conversation
from QLearning.QL_algorithm_after import Conversation

from QA_list_Before import QA_list_Before
from QA_list_After import QA_list_After

if __name__ == '__main__':
    # 이전 데이터가 없으면 조건 추가
    uid = input("uid 를 입력하세요.\n")
    folder = "Data/"
    file = folder + uid + ".txt"

    if os.path.isfile(file):
        print("historical data exits. -> after func execute.")
        after_func(file, uid)

    else:
        print("No historical data -> before func execute.")
        before_func(uid)

