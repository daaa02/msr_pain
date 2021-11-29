import numpy as np
from QLearning.env_before import Env

# 'Timing1',
before_slot_list = ['Greeting', 'Position', 'Quality', 'R_factor1', 'R_factor2', 'Severity',
                    'Timing2', 'Bedtime', 'Asleep', 'Disorder', 'Sleep1', 'Sleep2', 'Bye']  # frequency, term 추가

env = Env(before_slot_list)

Q = np.multiply(np.random.rand(env.state_len, env.action_len), 0.005)
# set learning parameters (learning rate lr, discount factor y [should be ~0.9])
lr = .50
y = .95
num_episodes = 5000    # 학습 횟수 50,000 -> 5,000 으로 변경: 속도 개선 된다는디

# create lists to contain total rewards and steps per episode
doneList = []
rList = []
tmp_rList = []
tmp_idx = 0


def qtable_out():
    # for si, row in enumerate(Q.tolist()):
    #     print(si, env.states[si], row)s
    return env.states, Q


for i in range(num_episodes):

    # reset environment and get first new observation
    s = env.resetenv()
    reward_all = 0
    d = False
    j = 0

    tmp_idx += 1

    # Q-Table learning algorithm
    while j < 20:
        j += 1

        # choose an action by greedily (with noise) picking from Q table
        # todo: reduced noise and disabled reducing randomness over time for more exploration
        a = np.argmax(np.multiply(Q[s, :] + np.random.randn(1, env.action_len) * (1. / (i + 1)), 0.5))  # * (1./(i+1))

        # get new state and reward from environment
        s1, r, d = env.step(a)

        # update Q-Table with new knowledge
        # according to Bellman eqn
        Q[s, a] = Q[s, a] + lr * (r + y * np.max(Q[s1, :]) - Q[s, a])
        reward_all += r
        s = s1

        # end convo?
        if d == True:

            if r > 0:
                doneList.append(1)
            else:
                doneList.append(0)

            break

    # jList.append(j)
    rList.append(reward_all)

    # for increment count
    tmp_rList.append(reward_all)

    if i % 500 == 0:    # 5,000 -> 500 으로 줄였음: 에피소드 수를 줄여서 얘도 걍 줄임
        # print("Score over time: " +  str(sum(rList)/num_episodes), i)
        # print("Score this increment: " + str(sum(tmp_rList) / tmp_idx), i)
        tmp_rList = []
        tmp_idx = 0

# print("number of succesful episodes: " + str(sum(doneList)) + "%")
# print("Final Q-Table Values")

print(before_slot_list)

qtable_out()