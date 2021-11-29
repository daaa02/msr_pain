import numpy as np
import itertools

class Env(object):

    def __init__(self, slot_list, noise_level=0.05, annoyance_level=7):
        self.slot_list = slot_list  # msr_ingestion 프로젝트에서는 env_slot_list 로 변경
        self.noise_level = noise_level
        self.annoyance = 0
        self.annoyance_level = annoyance_level

        self.i2x, self.x2i, self.states, self.state_idx = self.init_state_info(slot_list)

        self.current_state = np.copy(self.states[0])
        self.user_state = self.current_state
        self.order_state = np.copy(self.states[0])
        self.turnnumber = 0

        self.state_len = len(self.states)
        self.action_len = len(self.slot_list)

    def init_state_info(self, slot_list):   # msr_ingestion 프로젝트에서는 env_slot_list 로 변경
        # {0: 'Greeting', 1: 'Position', 2: 'Quality', 3: 'R_factor1', 4: 'R_factor2', 5: 'Severity', 6: 'Timing1', 7: 'Timing2', 8: 'Mood', 9: 'Anxiety', 10: 'Sleep1', 11: 'Sleep2', 12: 'Bye'}
        i2x = dict(enumerate(slot_list))    # msr_ingestion 프로젝트에서는 env_slot_list 로 변경
        # {'Greeting' :0 , 'Position' :1, 'Quality' : 2, 'R_factor1':3, 'R_factor2':4, 'Severity':5, 'Timing1':6, 'Timing2':7,'Mood':8, 'Anxiety':9, 'Sleep1':10, 'Sleep2':11, 'Bye':12}
        x2i = {v: k for k, v in list(enumerate(slot_list))} # msr_ingestion 프로젝트에서는 env_slot_list 로 변경

        # [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0], ...]
        _states = [list(i) for i in itertools.product([0, 1], repeat=len(slot_list))]
        # {'[0, 0, 0, 0, 0, 0, 0]': 0, '[0, 0, 0, 0, 0, 0, 1]': 1, '[0, 0, 0, 0, 0, 1, 0]': 2, ...}
        _state_idx = {str(v): k for k, v in list(enumerate(_states))}

        return i2x, x2i, _states, _state_idx

    def step(self, action):
        # update
        next_state, reward, hang_up, action_idx = self._user(action)
        # add noise output
        self.current_state = self._addnoise(next_state, action)
        self.turnnumber += 1

        return self.state_idx[str(self.current_state)], reward, hang_up

    def resetenv(self):
        self.current_state = np.copy(self.states[0]).tolist()
        self.user_state = self.current_state
        self.turnnumber = 0
        self.annoyance = 0

        return self.state_idx[str(self.current_state)]

    def _user(self, action):
        hang_up = False
        reward = 0
        last_state = np.copy(self.user_state).tolist()
        self.user_state[action] = 1
        self.order_state[action] = self.turnnumber
        action = self.i2x[action]  # action to string

        # 감점요인
        # 답변이 다 들어오지 않은 상태에서 Bye를 말하면 reward=-1
        if (action == 'Bye') and (0 in last_state[:self.x2i['Bye']]):
            self.annoyance += self.annoyance_level
            # hang_up = True
            reward -= 10
            # return self.user_state, reward, hang_up, self.x2i[action]

        # 통증 부위 답변이 들어오지 않았는데 다른 질문시 reward=-1
        if (action not in self.slot_list[:2]) and (last_state[self.x2i['Position']] == 0):
            self.annoyance += self.annoyance_level
            #hang_up = True
            reward -= 1
            #return self.user_state, reward, hang_up, self.x2i[action]

        # 통증부위나 통증 양상에 대한 답이 들어오지 않았는데 통증 강도 답변이 들어올 경우 reward = -1
        if (action not in self.slot_list[:3]) and last_state[self.x2i['Quality']] == 0:
            self.annoyance += self.annoyance_level
            #hang_up = True
            reward -= 1
            #return self.user_state, reward, hang_up, self.x2i[action]

        # if (action == 'R_factor' or action == 'Severity' or action == 'Timing') and (
        #         last_state[self.x2i['Position']] == 0 or last_state[self.x2i['Quality']] == 0):
        #     self.annoyance += self.annoyance_level
        #     hang_up = True
        #     reward -= 1
        #     return self.user_state, reward, hang_up, self.x2i[action]

        # 통증질문이 끝나지 않았는데 수면 질문 수행할 경우
        if (0 in last_state[:7]) and (
                action == 'Bedtime' or action == 'Asleep' or action == 'Disorder'
                or action == 'Sleep1' or action == 'Sleep2'):
            self.annoyance += self.annoyance_level
            reward -= 1


        # # Timing1은 Timing2 보다 먼저 질문해야함
        # if (action == 'Timing2' and last_state[self.x2i['Timing1']] == 0):
        #     self.annoyance += self.annoyance_level
        #     #hang_up = True
        #     reward -= 1
        #     #return self.user_state, reward, hang_up, self.x2i[action]
        # #


        # R_factor1,2와 Sleep1,2는 순서는 상관없지만 연달아 질문해야 함
        if (last_state[self.x2i['R_factor1']] == 1 and last_state[self.x2i['R_factor2']] == 0 and action != 'R_factor2') \
                or (last_state[self.x2i['R_factor1']] == 0 and last_state[self.x2i['R_factor2']] == 1 and action != 'R_factor1'): #\
                # or (last_state[self.x2i['Timing1']] == 1 and last_state[self.x2i['Timing2']] == 0 and action != 'Timing2'):
            self.annoyance += self.annoyance_level
            hang_up = True
            reward -= 1
            return self.user_state, reward, hang_up, self.x2i[action]

        if (last_state[self.x2i['Sleep1']] == 1 and last_state[self.x2i['Sleep2']] == 0 and action != 'Sleep2') \
                or (last_state[self.x2i['Sleep1']] == 0 and last_state[self.x2i['Sleep2']] == 1 and action != 'Sleep1'):
            self.annoyance += self.annoyance_level
            hang_up = True
            reward -= 1
            return self.user_state, reward, hang_up, self.x2i[action]



        # if no greeting in the first few turns, penalize (minor)
        if action != 'Greeting' and self.turnnumber < 1 and last_state[self.x2i['Greeting']] == 0:
            self.annoyance += 1
            reward -= 1

        # if give greeting after the first few turns, penalize (moderate)
        if action == 'Greeting' and self.turnnumber > 1:
            self.annoyance += 6
            reward -= 1

        # # if goodbye without 'anything else', penalize (minor)
        # if action == 'Bye' and last_state[self.x2i['Anything_else']] == 0:
        #     self.annoyance += 1

        # i.e. asking repeat questions
        if last_state[self.x2i[action]] == 1:
            self.annoyance += 5

        # 가점 요인
        # MINOR PLEASANTRIES
        # if do greeting in the first few turns, add small reward
        if action == 'Greeting' and self.turnnumber < 2:
            reward += 0.1

        if action == 'Position' and (last_state[self.x2i['Position']] == 0) \
                and last_state[self.x2i['Greeting']] == 1 \
                and last_state[2:] == 0:
            reward += 0.1

        if (action == 'R_factor1' and (last_state[self.x2i['R_factor1']] == 0)) \
                or (action == 'R_factor2' and (last_state[self.x2i['R_factor2']] == 0)) \
                or (action == 'Severity' and (last_state[self.x2i['Severity']] == 0)) \
                or (action == 'Timing2' and (last_state[self.x2i['Timing2']] == 0)) \
                and last_state[self.x2i['Greeting']] == 1 \
                and last_state[self.x2i['Position']] == 1 \
                and last_state[self.x2i['Bye']] == 0:
            reward += 0.1

        # or (action == 'Timing1' and (last_state[self.x2i['Timing1']] == 0)) \ Timing1 사용시 위에 이걸로 변경

        # Quality 질문을 3번째로 하면 reward
        if action == 'Quality' and (last_state[self.x2i['Quality']] == 0) \
                and last_state[:2] == 1 and last_state[2:] == 0:
            reward += 0.1

        # 통증 질문이 끝난 후 스트레스 질문을 하면 reward
        if (action == 'Bedtime' or action == 'Asleep' or action == 'Disorder' or action == 'Sleep1' or action == 'Sleep2') \
                and last_state[:self.x2i['Bedtime']] == 1:
            reward += 0.1


        # # 스트레스 질문 중 Mood 질문을 먼저하면 reward
        # if (action == 'Mood' and last_state[self.x2i['Mood']] == 0) and (1 not in last_state[9:]):
        #     reward += 0.1

        # Bedtime 질문을 Asleep 질문보다 먼저 하면 reward
        if action == 'Bedtime' and last_state[self.x2i['Asleep']] == 0 and last_state[self.x2i['Bedtime']] == 1:
            reward += 0.1


        # 중단 or 완료
        if self.annoyance > self.annoyance_level:
            hang_up = True
            reward -= 1
            return self.user_state, reward, hang_up, self.x2i[action]

        # if action == 'Anything_else' and (last_state[self.x2i['Anything_else']] == 0) \
        #         and last_state[self.x2i['Greeting']] == 1 \
        #         and last_state[self.x2i['Position']] == 1 \
        #         and last_state[self.x2i['R_factor']] == 1 \
        #         and last_state[self.x2i['Severity']] == 1 \
        #         and last_state[self.x2i['Timing']] == 1 \
        #         and last_state[self.x2i['Bye']] == 0:
        #     reward += 0.1

        if action == 'Bye' and last_state[self.x2i['Bye']] == 0 and (0 not in last_state[:self.x2i['Bye']]):
            hang_up = True
            reward += 1000
            return self.user_state, reward, hang_up, self.x2i[action]

        # and last_state[self.x2i['Greeting']] == 1 \
        # and last_state[self.x2i['Position']] == 1 \
        # and last_state[self.x2i['R_factor1']] == 1 \
        # and last_state[self.x2i['R_factor2']] == 1 \
        # and last_state[self.x2i['Severity']] == 1 \
        # and last_state[self.x2i['Timing1']] == 1 \
        # and last_state[self.x2i['Timing2']] == 1 \
        # and last_state[self.x2i['Mood']] == 1 \
        # and last_state[self.x2i['Anxiety']] == 1 \
        # and last_state[self.x2i['Sleep1']] == 1 \
        # and last_state[self.x2i['Sleep2']] == 1:


        # elif action == 'Bye' and (last_state[self.x2i['Bye']] == 0) \
        #         and last_state[self.x2i['Greeting']] == 1 \
        #         and last_state[self.x2i['Position']] == 1 \
        #         and last_state[self.x2i['R_factor']] == 1 \
        #         and last_state[self.x2i['Severity']] == 1 \
        #         and last_state[self.x2i['Timing']] == 1 \
        #         and last_state[self.x2i['Anything_else']] == 0:
        #     hang_up = True
        #     reward = 100
        #     return self.user_state, reward, hang_up, self.x2i[action]

        return self.user_state, reward, hang_up, self.x2i[action]

    def _addnoise(self, state, action):

        flip_idx = action

        while self.i2x[flip_idx] not in ['Bye', self.i2x[action]]:
            flip_idx = np.random.randint(0, len(self.slot_list))

        chance = np.random.random()

        if chance <= self.noise_level:
            state[action] = 0  # 노이즈로 값 바꾸면 state[action]도 undo

            if state[flip_idx] == 0:
                state[flip_idx] = 1

            else:
                state[flip_idx] = 1

        return state
