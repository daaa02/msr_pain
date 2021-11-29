class QA_list_After:

    before_slot_list = ['Greeting', 'Position', 'Quality', 'R_factor1', 'R_factor2', 'Severity',
                        'Timing2', 'Bedtime', 'Asleep', 'Disorder', 'Sleep1', 'Sleep2', 'Bye']

    before_question_list = \
        {
            'Greeting': ['안녕하세요. 지금부터 문진을 시작할게요.',
                         '안녕하세요. 저는 문진 로봇입니다. 지금부터 저의 질문에 답해주세요.',
                         '안녕하세요. 저는 문진 로봇이에요. 지금부터 문진을 시작할게요.'],

            # 통증 문진
            'Position': ['현재 제일 아픈 부위가 어디인가요?',
                         '지금 어느 부위가 가장 아프신가요?',
                         '지금 가장 불편한 곳이 어디인가요?'],

            'Quality': ['통증이 어떻게 느껴지시나요? 저린다, 욱씬거린다와 같이 표현해주세요.',
                        '어떤 식으로 아프신가요? 저리다, 쑤신다와 같이 표현해 주세요.',
                        '어떤 통증이 느껴지시나요? 저리다, 욱씬거리다와 같이 표현해주세요.'],

            'R_factor1': ['하루 중에 언제 가장 아픈가요?',
                          '통증이 가장 심해지는 시간대는 언제인가요?',
                          '특별히 통증이 심해지는 시간대가 있으신가요? 아침, 자기 전과 같이 대답해주세요.'],

            'R_factor2': ['어떤 자세일 때 가장 아픈가요?',
                          '무슨 자세를 취하면 가장 아픈가요?',
                          '통증이 어떤 자세에서 심해지나요?'],

            'Severity': ['통증이 얼마나 심한지 0에서 10점 사이로 답해주세요.',
                         '통증을 0부터 10 사이의 숫자로 표현하신다면 몇 점 쯤 되나요?',
                         '0부터 10사이의 숫자로 얼마나 아픈지 표현해 주시겠어요?'],

            'Timing2': ['통증이 심해진 기간은 며칠 정도 되었나요? 1일, 1주일과 같이 대답해주세요.',
                        '통증이 심해진 지는 얼마나 되었나요? 1일, 1주일과 같이 기간으로 대답해주세요.',
                        '최근 통증이 심해진 기간은 어느정도 되었나요? 1일, 1주일과 같이 대답해주세요.'],

            # 수면 문진
            'Bedtime': ['지난 한 달 동안, 보통 몇 시쯤 잠자리에 드셨나요?.'],

            'Asleep': ['지난 한 달 동안, 잠자리에 든 후 잠들기까지 몇 분쯤 걸렸나요?'],

            'Disorder': ['지난 한 달 동안, 수면 장애로 인해 낮 동안의 활동에 지장을 받은 경우가 얼마나 자주 있으셨나요?'
                         '없음, 가끔, 자주 중에서 대답해주세요.'],

            'Sleep1': ['잠은 몇 시간 정도 주무셨나요?',
                       '어제 밤엔 몇 시간 주무셨나요?'],

            'Sleep2': ['잠은 안 깨고 잘 주무셨나요?',
                       '잠은 중간에 깨지 않고 잘 주무셨나요?',
                       '수면의 질에 관한 질문입니다. 자는 도중 깨지 않고 잘 주무셨나요?'],

            'Bye': ['문진이 종료되었습니다. 문진 결과를 알려 드리겠습니다.',
                    '그럼 문진 결과를 알려 드리겠습니다.',
                    '문진이 끝났습니다. 문진 결과 알려드릴게요.']
        }

    after_slot_list = ['Greeting', 'Position', 'Quality', 'R_factor1', 'R_factor2', 'Severity',
                       'Timing2', 'Bedtime', 'Asleep', 'Disorder', 'Sleep1', 'Sleep2', 'Bye']
    # 'Position_Before', 'Severity_Before' 쓸거면 추가하기
    after_question_list = \
        {
            'Greeting': ['안녕하세요. 문진 시간이에요. 우선 지난 문진 결과를 알려드린 후 문진을 시작할게요.',
                         '안녕하세요. 저는 문진 로봇입니다. 우선 당신의 지난 문진 결과를 알려드리겠습니다.',
                         '안녕하세요. 저는 문진 로봇이에요. 당신의 지난 문진 결과를 알려드린 후 문진을 시작할게요.'],

            # 통증 문진
            'Position': ['현재 제일 아픈 부위가 어디인가요?',
                         '지금 어느 부위가 가장 아프신가요?',
                         '지금 가장 불편한 곳이 어디인가요?'],

            'Quality': ['통증이 어떻게 느껴지시나요? 저린다, 욱씬거린다와 같이 표현해주세요.',
                        '어떤 식으로 아프신가요? 저리다, 쑤신다와 같이 표현해 주세요.',
                        '어떤 통증이 느껴지시나요? 저리다, 욱씬거리다와 같이 표현해주세요.'],

            'R_factor1': ['하루 중에 언제 가장 아픈가요?',
                          '통증이 가장 심해지는 시간대는 언제인가요?',
                          '특별히 통증이 심해지는 시간대가 있으신가요? 아침, 자기 전과 같이 대답해주세요.'],

            'R_factor2': ['어떤 자세일 때 가장 아픈가요?',
                          '무슨 자세를 취하면 가장 아픈가요?',
                          '통증이 어떤 자세에서 심해지나요?'],

            'Severity': ['통증이 얼마나 심한지 0에서 10점 사이로 답해주세요.',
                         '통증을 0부터 10 사이의 숫자로 표현하신다면 몇 점 쯤 되나요?',
                         '0부터 10사이의 숫자로 얼마나 아픈지 표현해 주시겠어요?'],

            'Timing2': ['통증이 심해진 기간은 며칠 정도 되었나요? 1일, 1주일과 같이 대답해주세요.',
                        '통증이 심해진 지는 얼마나 되었나요? 1일, 1주일과 같이 기간으로 대답해주세요.',
                        '최근 통증이 심해진 기간은 어느정도 되었나요? 1일, 1주일과 같이 대답해주세요.'],

            # 수면 문진
            'Bedtime': ['지난 한 달 동안, 보통 몇 시쯤 잠자리에 드셨나요?.'],

            'Asleep': ['지난 한 달 동안, 잠자리에 든 후 잠들기까지 몇 분쯤 걸렸나요?'],

            'Disorder': ['지난 한 달 동안, 수면 장애로 인해 낮 동안의 활동에 지장을 받은 경우가 얼마나 자주 있으셨나요?'
                         '없음, 가끔, 자주 중에서 대답해주세요.'],

            'Sleep1': ['잠은 몇 시간 정도 주무셨나요?',
                       '어제 밤엔 몇 시간 주무셨나요?'],

            'Sleep2': ['잠은 안 깨고 잘 주무셨나요?',
                       '잠은 중간에 깨지 않고 잘 주무셨나요?',
                       '수면의 질에 관한 질문입니다. 자는 도중 깨지 않고 잘 주무셨나요?'],

            'Bye': ['문진이 종료되었습니다. 문진 결과를 알려 드리겠습니다.',
                    '그럼 문진 결과를 알려 드리겠습니다.',
                    '문진이 끝났습니다. 문진 결과 알려드릴게요.']
        }

    def before_final_output(slot):
        for i in range(len(slot)):
            word = "당신의 통증 부위는 "
            for i in range(len(slot['Position'])):
                word += str(slot['Position'][i])
                if i != (len(slot['Position']) - 1):
                    word += ', '
                else:
                    word += '이고, '
            for i in range(len(slot['Quality'])):
                word += str(slot['Quality'][i])
                if i != (len(slot['Quality']) - 1):
                    word += ', '
                else:
                    word += ' 증상이 있으며, '
            if 'R_factor1' in slot.keys():
                for i in range(len(slot['R_factor1'])):
                    word += str(slot['R_factor1'][i]) + ', '
            for i in range(len(slot['R_factor2'])):
                word += str(slot['R_factor2'][i])
                if i != (len(slot['R_factor2']) - 1):
                    word += ', '
                else:
                    word += ' 증상이 심해지고, '

            word += '통증의 강도는 ' + str(slot['Severity']) + '이며, ' + str(slot['Timing2']) + ' 전부터 통증이 심해졌군요.'
            word += '\n그리고 당신은 보통 ' + str(slot['Bedtime']) + '시에 잠자리에 드셨고, 잠들기까지 약 ' + str(slot['Asleep'])
            word += '정도 걸렸으며 ' + str(slot['Sleep1']) + '시간 주무셨습니다.\n'
            word += '수면의 질은 ' + str(slot['Sleep2']) + '이고, 수면 장애로 인해 일상생활에 불편함을 겪은 적이 ' + str(slot['Disorder'])
            word += '이라고 답하셨습니다. 감사합니다.'

        print(word)
        return word

    def before_result(result):
        data = []
        word = "당신은 이전 문진에서 "
        if 'Position' in result.keys():
            data = result['Position'].split(',')
            for i in range(len(data)):
                word += str(data[i])
                if i != (len(data) - 1):
                    word += ','
                else:
                    word += '에 '
        data.clear()

        if 'Quality' in result.keys():
            data = result['Quality'].split(',')
            for i in range(len(data)):
                word += str(data[i])
                if i != (len(data) - 1):
                    word += ','
                else:
                    word += ' 증상이 있으며, '
            data.clear()

        if 'R_factor1' in result.keys() and 'R_factor2' in result.keys():
            data = result['R_factor1'].split(',')
            for i in range(len(data)):
                word += str(data[i]) + ","
            data.clear()
            data = result['R_factor2'].split(',')
            for i in range(len(data)):
                word += " " + str(data[i])
                if i != (len(data) - 1):
                    word += ','
                else:
                    word += ' 증상이 심해졌고, '
            data.clear()
        elif 'R_factor1' in result.keys() and 'R_factor2' not in result.keys():
            data = result['R_factor1'].split(',')
            for i in range(len(data)):
                word += str(data[i])
                if i != (len(data) - 1):
                    word += ','
                else:
                    word += '에 증상이 심해졌고, '
            data.clear()
        elif 'R_factor1' not in result.keys() and 'R_factor2' in result.keys():
            data = result['R_factor2'].split(',')
            for i in range(len(data)):
                word += str(data[i])
                if i != (len(data) - 1):
                    word += ','
                else:
                    word += ' 증상이 심해졌고, '
            data.clear()

        if 'Severity' in result.keys():
            word += '통증의 강도는 ' + str(result['Severity']) + '이며, '
        if 'Timing2' in result.keys():
            word += '통증이 지속된 기간은 ' + str(result['Timing2']) + '라고 답하셨습니다.'
        if 'Bedtime' in result.keys():
            word += '\n그리고 당신은 잠자리에 ' + str(result['Bedtime']) + '시에 드셨고, '
        if 'Asleep' in result.keys():
            word += '잠들기까지 약 ' + str(result['Asleep']) + '정도 걸리며,'
        if 'Sleep1' in result.keys():
            word += '잠은 ' + str(result['Sleep1']) + '시간 주무셨다고 답하셨네요. '
        if 'Sleep2' in result.keys():
            word += '수면의 질은 ' + str(result['Sleep2']) + ', '
        if 'Disorder' in result.keys():
            word += '수면 장애로 인해 일상생활에 불편함을 겪은 적이 ' + str(result['Disorder']) + '이라고 답하셨습니다.'

        print(word)
        return word

    def before_position(result):

        if 'Position' in result.keys():
            word = "당신은 이전 문진에서 "
            word += str(result['Position']) + ' 부위에 통증을 느끼셨다고 답하셨는데,  \n'

        return word

    def before_severity(result):

        if 'Severity' in result.keys():
            word = str(result['Position']) + ' 부위의 통증 강도가 ' + str(result['Severity']) + ' 정도라고 답하셨습니다. 지금은 \n'

        return word

    def now_position(slot):

        for i in range(len(slot)):
            word = "현재 "
            for i in range(len(slot['Position'])):
                word += str(slot['Position'][i])
                word += '부위 '

        return word

    def fb_position(slot):

        for i in range(len(slot)):
            word = "네, 지금 "
            for i in range(len(slot['Position'])):
                word += str(slot['Position'][i]) + " 부위가 불편하시군요. \n"

        return word

    def fb_factor2(slot):

        for i in range(len(slot)):
            word = "네. "
            for i in range(len(slot['R_factor2'])):
                word += str(slot['R_factor2'][i])
                if i != (len(slot['R_factor2']) - 1):
                    word += ', '
                else:
                    word += " 증상이 더 심해지시네요. \n"

        return word

    def fb_severity(slot):

        severity = int(slot['Severity'])
        if severity >= 7:
            word = "네, 통증이 심하시군요. \n"
        else:
            word = "네, 많이 불편하셨겠네요. \n"

        return word
