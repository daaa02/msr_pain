from QLearning.env_after import Env
from QA_list_After import QA_list_After
import random
from datetime import datetime, date, time


class Conversation(object):
    def __init__(self, slot_list):
        self.slot_list = slot_list  # msr_ingestion 프로젝트에서는 env_slot_list 로 변경
        self.env = Env(self.slot_list)  # msr_ingestion 프로젝트에서는 env_slot_list 로 변경
        self.user_state = self.env.user_state
        self.state_Q = []
        self.current_Q = []
        self.action_idx = None
        self.action = None

    def state_Q_list(self, Q):
        for i, row in enumerate(Q.tolist()):
            self.state_Q.append([self.env.states[i], row])

    def update(self):
        idx_current_Q = []
        for i in range(len(self.state_Q)):
            if self.user_state.tolist() == self.state_Q[i][0]:
                self.current_Q = self.state_Q[i][1]

                # for n in range(len(self.state_Q[i][1])):
                #     self.current_Q.append([n, self.state_Q[i][1][n]])

        # 확률 순서대로 정렬, 확률 같을 경우 동일 확률 action 중에 랜덤으로 수행
        # print(self.current_Q)

        for i, num in enumerate(self.current_Q):
            idx_current_Q.append([i, num])
        idx_current_Q.sort(key=lambda x: x[1], reverse=True)
        # print("idx_current_Q = {}".format(idx_current_Q))

        if idx_current_Q[0][1] == idx_current_Q[1][1]:
            if idx_current_Q[1][1] == idx_current_Q[2][1]:
                self.action_idx = random.choice([idx_current_Q[0][0], idx_current_Q[1][0], idx_current_Q[2][0]])
            else:
                self.action_idx = random.choice([idx_current_Q[0][0], idx_current_Q[1][0]])
        else:
            self.action_idx = idx_current_Q[0][0]

        # print("action_idx = {}".format(self.action_idx))

        self.action = self.env.i2x[self.action_idx]  # action_idx to string
        self.user_state[self.action_idx] = 1  # user_state update
        # print(self.user_state)

    def make_slot(self, slot, action, result):  # ID 받는거 추가해야함, 통증 부위 개수에 따라 slot 만드는 함수
        # dic_tmp = {action : result}
        # print(result)
        slot[action] = result
        # slot.append(dic_tmp)
        return slot

    def save_text(self, slot, uid):  # 최종 slot 텍스트로 저장
        folder = "Data/"
        date_day = date(datetime.today().year, datetime.today().month, datetime.today().day)
        date_time = time(hour=datetime.today().hour, minute=datetime.today().minute, second=datetime.today().second)
        file_name = folder + uid + ".txt"  # "_" + str(date) +
        file = open(file_name, 'w')  # 이전 문진 기록 밑에 계속 쓰기 -> 하니까 parsing 불가해져서 다시 w로 바꿈
        file.write("Date:" + str(date_day) + " " + str(date_time) + "\n")
        for i in range(1, (len(QA_list_After.before_slot_list) - 1)):

            if i < len(QA_list_After.before_slot_list) - 2:
                if QA_list_After.before_slot_list[i] in slot:
                    file.write(str(QA_list_After.before_slot_list[i]) + ':' + str(
                        slot[QA_list_After.before_slot_list[i]]) + "\n")
                    # print(QA_list_After.before_slot_list[i])
                    # print(slot[QA_list_After.before_slot_list[i]])
            else:
                if QA_list_After.before_slot_list[i] in slot:
                    file.write(
                        str(QA_list_After.before_slot_list[i]) + ':' + str(slot[QA_list_After.before_slot_list[i]]))
