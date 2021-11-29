from multiprocessing import Process
from before_func import before_func
from after_func import after_func
from transcribe_streaming_infinite import tts
import os.path

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

    # # p1 = Process(target=tts)
    # # p2 = Process(target=after_func, args=(file, uid))
    # # p3 = Process(target=before_func)
    #
    # p1.start()

    if os.path.isfile(file):
        print("historical data exits. -> after func execute.")
        # p2.start()
        #
        # p2.join()
        # p1.join()
        after_func(file, uid)

    else:
        print("No historical data -> before func execute.")
        # p3.start()
        #
        # p3.join()
        # p1.join()
        before_func(uid)

