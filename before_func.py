def before_func(uid):
    import os
    import random
    import time
    import csv
    from connect import Connection
    from QLearning.qtable_before import qtable_out
    from NLP import NLP, Dictionary
    from QA_list_Before import QA_list_Before
    from QLearning.QL_algorithm_before import Conversation
    from transcribe_streaming_mic import speech_to_text

    # init variables
    slot = {}
    states, Q = qtable_out()
    # explicit()  # google credential
    nlp = NLP()
    dic = Dictionary()
    connect = Connection()
    text_to_speech = connect.tts_connect()

    # connect
    assistant, assistant_info, session_id = connect.assistant_connect('ef4292f2-8274-48d6-bee1-20b20f18a63c')

    # Kakao tts api
    def tts(speech_text):
        file = "tts.wav"
        connect.tts(f"<speak>\
                    <voice name='WOMAN_READ_CALM'><prosody rate='medium'>{speech_text}<break time='500ms'/></prosody></voice>\
                    </speak>", file)
        connect.play(file, 'local', '-1000', False)
        print("\n")
        # print(speech_text)

    # csv 저장 관련
    folder = "Data/"
    csv_file = open(f'{folder}/{uid}_turn.csv', 'a', newline='')
    cw = csv.writer(csv_file)

    rej = []

    # 첫번째 질문 수행하기(Greeting)
    conversation = Conversation(QA_list_Before.before_slot_list)
    conversation.state_Q_list(Q)
    conversation.update()
    out = random.choice(QA_list_Before.before_question_list[conversation.action])
    print(conversation.action, conversation.action_idx)
    print(conversation.user_state)
    print(out + '\n')  # 질문 출력
    tts(out)

    cw.writerow(['msr', out])
#     # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

    # 두번째 질문 수행하기(Position)
    conversation.update()
    out = random.choice(QA_list_Before.before_question_list[conversation.action])
    print(conversation.action, conversation.action_idx)
    print(conversation.user_state)
    print(out + '\n')  # 질문 출력
    tts(out)
    cw.writerow(['msr', out])
    # print('\n')
    # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

    while conversation.user_state.tolist() != conversation.state_Q[len(conversation.state_Q) - 1][0]:
        if conversation.action == 'Position':
            start = time.time()
            user_in = speech_to_text()  # 완료 시 엔터 입력!
            # user_in = input()
            cw.writerow(['user', user_in])

            pain_point = nlp.nlp_position(user_in, dic)
            print("pain_point = {}".format(pain_point))
            print(f'({time.time() - start:.3f}sec)' + '\n')

            if len(pain_point) != 0:
                conversation.make_slot(slot=slot, action=conversation.action, result=pain_point)
                conversation.update()
                out = QA_list_Before.fb_position(slot)
                out += random.choice(QA_list_Before.before_question_list[conversation.action])

                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

            else:
                rej.append("rejection")
                out = "잘 못들었습니다." + random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

        if conversation.action == 'Quality':
            start = time.time()
            user_in = speech_to_text()  # 완료 시 엔터 입력!
            # user_in = input()
            cw.writerow(['user', user_in])

            response = assistant.message(
                assistant_id=assistant_info['assistant_id'],
                session_id=session_id,
                input={
                    'message_type': 'text',
                    'text': user_in
                }
            ).get_result()['output']

            quality = []
            # print(response["intents"])
            [quality.append(response["intents"][i]["intent"]) for i in range(len(response["intents"])) if
             response["intents"][i]["confidence"] > 0.5]
            print("pain_quality = {}".format(quality) + '\n')
            print(f'({time.time() - start:.3f}sec)' + '\n')

            if len(quality) != 0:
                conversation.make_slot(slot=slot, action=conversation.action, result=quality)
                conversation.update()
                out = "네, 그러시군요. \n"
                out += random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

            else:
                rej.append("rejection")
                out = "잘 못들었습니다." + random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

        if conversation.action == 'R_factor1':
            start = time.time()
            user_in = speech_to_text()  # 완료 시 엔터 입력!
            # user_in = input()
            cw.writerow(['user', user_in])

            response = assistant.message(
                assistant_id=assistant_info['assistant_id'],
                session_id=session_id,
                input={
                    'message_type': 'text',
                    'text': user_in
                }
            ).get_result()['output']  # 밤에 자기 전에 많이 아파요.

            r_tmp1 = []
            r_tmp2 = []
            r_tmp3 = []
            [r_tmp1.append(response["entities"][i]["value"]) for i in range(len(response["entities"])) if
             response["entities"][i]["entity"] == "특정시간대"]
            [r_tmp2.append(response["entities"][i]["value"]) for i in range(len(response["entities"])) if
             response["entities"][i]["entity"] == "특정통증상황"]
            [r_tmp3.append(response["entities"][i]["value"]) for i in range(len(response["entities"])) if
             response["entities"][i]["entity"] == "부정어"]
            # print(response["entities"])
            # [print(response["entities"][i]["value"]) for i in range(len(response["entities"]))]

            if len(r_tmp1) != 0:
                r_factor1 = list(set(r_tmp1))  # 중복값 제거
                conversation.make_slot(slot=slot, action=conversation.action, result=r_factor1)
                # print(conversation.action)
                print("r_factor1 = {}".format(r_factor1) + '\n')
                print(f'({time.time() - start:.3f}sec)' + '\n')

                conversation.update()
                out = random.choice(QA_list_Before.before_question_list[conversation.action])

            elif len(r_tmp2) != 0:
                r_factor2 = list(set(r_tmp2))  # 중복값 제거
                conversation.make_slot(slot=slot, action='R_factor2', result=r_factor2)
                print("r_factor2 = {}".format(r_factor2) + '\n')
                print(f'({time.time() - start:.3f}sec)' + '\n')
                conversation.user_state[
                    conversation.env.x2i['R_factor2']] = 1  # R_factor1 질문에 R_factor2 답을 했을 때 R_factor 질문 끝내고 넘어감
                conversation.update()
                out = random.choice(QA_list_Before.before_question_list[conversation.action])

            elif len(r_tmp3) != 0 and len(r_tmp1) == 0 and len(r_tmp2) == 0:
                conversation.user_state[
                    conversation.env.x2i['R_factor1']] = 1  # 통증이 심해지는 시간대가 없다고 답하면 통증이 심해지는 자세 질문으로 넘어감
                conversation.update()
                out = random.choice(QA_list_Before.before_question_list[conversation.action])

            else:
                rej.append("rejection")
                out = "잘 못들었습니다." + random.choice(QA_list_Before.before_question_list[conversation.action])

            print(conversation.action, conversation.action_idx)
            print(conversation.user_state)
            print(out + '\n')  # 질문 출력
            tts(out)
            cw.writerow(['msr', out])
            # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

        if conversation.action == 'R_factor2':
            start = time.time()
            user_in = speech_to_text()  # 완료 시 엔터 입력!
            # user_in = input()
            cw.writerow(['user', user_in])

            response = assistant.message(
                assistant_id=assistant_info['assistant_id'],
                session_id=session_id,
                input={
                    'message_type': 'text',
                    'text': user_in
                }
            ).get_result()['output']  # 일어나서 몸을 일으켜 세울 때 많이 아파요.
            r_tmp2 = []
            [r_tmp2.append(response["entities"][i]["value"]) for i in range(len(response["entities"])) if
             response["entities"][i]["entity"] == "특정통증상황"]
            # print("r_tmp2 = ", r_tmp2)
            if any("물건 들 때" in i for i in r_tmp2) and any("휠체어로 옮겨 탈 때" in j for j in r_tmp2):
                r_tmp2.remove('물건 들 때')
            if len(r_tmp2) != 0:
                r_factor2 = list(set(r_tmp2))
                if 'R_factor1' not in slot:
                    conversation.user_state[
                        conversation.env.x2i['R_factor1']] = 1  # R_factor2 질문에 답하면 R_factor1 질문 안하고 넘어감
                conversation.make_slot(slot=slot, action=conversation.action, result=r_factor2)
                print("r_factor2 = {}".format(r_factor2) + '\n')
                print(f'({time.time() - start:.3f}sec)' + '\n')

                conversation.update()
                out = QA_list_Before.fb_factor2(slot)
                out += random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

            else:
                rej.append("rejection")
                out = "잘 못들었습니다." + random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

        if conversation.action == 'Severity':
            start = time.time()
            user_in = speech_to_text()  # 완료 시 엔터 입력!
            # user_in = input()
            cw.writerow(['user', user_in])

            # tmp = nlp.nlp_severity(user_in=user_in, dic=dic)
            severity = nlp.nlp_severity(user_in=user_in, dic=dic)
            print("severity = {}".format(severity) + '\n')
            print(f'({time.time() - start:.3f}sec)' + '\n')

            if len(severity) != 0:
                # severity = max(tmp)
                conversation.make_slot(slot=slot, action=conversation.action, result=severity)
                # print("severity = {}".format(severity) + '\n')
                conversation.update()

                out = QA_list_Before.fb_severity(slot)
                out += random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

            else:
                rej.append("rejection")
                out = "잘 못들었습니다." + random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

        if conversation.action == 'Timing2':
            start = time.time()
            user_in = speech_to_text()  # 완료 시 엔터 입력!
            # user_in = input()
            cw.writerow(['user', user_in])

            response = assistant.message(
                assistant_id=assistant_info['assistant_id'],
                session_id=session_id,
                input={
                    'message_type': 'text',
                    'text': user_in
                }
            ).get_result()['output']
            tmp = []
            timing = []

            for i in range(len(response["entities"])):
                if response["entities"][i]["entity"] == "통증기간":
                    # print("i = " , i)
                    # print(response["entities"][i])
                    # print(response["entities"][i]["value"])
                    for j in range(len(response["entities"][i]["value"])):
                        if response["entities"][i]["value"][j] == '년':
                            tmp.append(
                                [response["entities"][i]["value"], (int(response["entities"][i]["value"][:j]) * 365)])
                        elif response["entities"][i]["value"][j - 1] == '개' and response["entities"][i]["value"][
                            j] == '월':
                            tmp.append(([response["entities"][i]["value"],
                                         int(response["entities"][i]["value"][:(j - 1)]) * 30]))
                        elif response["entities"][i]["value"][j] == '주':
                            tmp.append(
                                [response["entities"][i]["value"], (int(response["entities"][i]["value"][:j]) * 7)])
                        elif response["entities"][i]["value"][j] == '일':
                            tmp.append(
                                [response["entities"][i]["value"], int(response["entities"][i]["value"][:j]) * 1])
            # print(tmp)
            if len(tmp) != 0:
                tmp.sort(key=lambda x: x[1], reverse=True)
                timing = tmp[0][0]
                conversation.make_slot(slot=slot, action=conversation.action, result=timing)
                print("timing = {}".format(timing) + '\n')
                print(f'({time.time() - start:.3f}sec)' + '\n')

                conversation.update()
                out = "네, 그러시군요. \n"
                out += random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

            else:
                rej.append("rejection")
                out = "잘 못들었습니다." + random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

        if conversation.action == 'Bedtime':
            start = time.time()
            user_in = speech_to_text()  # 완료 시 엔터 입력!
            # user_in = input()
            cw.writerow(['user', user_in])

            bedtime = nlp.nlp_sleep_time(user_in=user_in, dic=dic)
            print("bedtime = {}".format(bedtime) + '\n')
            print(f'({time.time() - start:.3f}sec)' + '\n')

            if bedtime != -1:
                conversation.make_slot(slot=slot, action=conversation.action, result=str(bedtime))
                conversation.update()
                out = "알겠습니다. \n"
                out += random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

            else:
                rej.append("rejection")
                out = "잘 못들었습니다. " + random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

        if conversation.action == 'Asleep':
            start = time.time()
            user_in = speech_to_text()  # 완료 시 엔터 입력!
            # user_in = input()
            cw.writerow(['user', user_in])

            response = assistant.message(
                assistant_id=assistant_info['assistant_id'],
                session_id=session_id,
                input={
                    'message_type': 'text',
                    'text': user_in
                }
            ).get_result()['output']
            tmp = []

            [tmp.append(response["entities"][i]["value"]) for i in range(len(response["entities"]))
             if response["entities"][i]["entity"] == "시간"]

            if len(tmp) >= 1:
                asleep_time = max(tmp)
                conversation.make_slot(slot=slot, action=conversation.action, result=asleep_time)
                print("asleep_time = {}".format(asleep_time) + '\n')
                print(f'({time.time() - start:.3f}sec)' + '\n')

                conversation.update()
                out = "그렇군요. \n"
                out += random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

            else:
                rej.append("rejection")
                out = "잘 못들었습니다." + random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

        if conversation.action == 'Disorder':
            start = time.time()
            user_in = speech_to_text()  # 완료 시 엔터 입력!
            # user_in = input()
            cw.writerow(['user', user_in])

            response = assistant.message(
                assistant_id=assistant_info['assistant_id'],
                session_id=session_id,
                input={
                    'message_type': 'text',
                    'text': user_in
                }
            ).get_result()['output']
            tmp = []
            disorder = []
            for i in range(len(response["intents"])):
                if response["intents"][i]["intent"] == '지장_없음' and response["intents"][i]["confidence"] > 0.5:
                    tmp.append(["없음", response["intents"][i]["confidence"]])
                elif response["intents"][i]["intent"] == '지장_가끔' and response["intents"][i]["confidence"] > 0.5:
                    tmp.append(["가끔 있음", response["intents"][i]["confidence"]])
                elif response["intents"][i]["intent"] == '지장_자주' and response["intents"][i]["confidence"] > 0.5:
                    tmp.append(["자주 있음", response["intents"][i]["confidence"]])

            if len(tmp) >= 1:
                disorder = max(tmp, key=lambda x: x[1])[0]
                print("disorder = {}".format(disorder) + '\n')
                print(f'({time.time() - start:.3f}sec)' + '\n')

                conversation.make_slot(slot=slot, action=conversation.action, result=disorder)
                conversation.update()
                out = random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

            else:
                rej.append("rejection")
                out = "잘 못들었습니다." + random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

        if conversation.action == 'Sleep1':
            start = time.time()
            user_in = speech_to_text()  # 완료 시 엔터 입력!
            # user_in = input()
            cw.writerow(['user', user_in])

            sleep_time = nlp.nlp_sleep_time(user_in=user_in, dic=dic)
            print("sleep_time = {}".format(sleep_time) + '\n')
            print(f'({time.time() - start:.3f}sec)' + '\n')

            if sleep_time != -1:
                conversation.make_slot(slot=slot, action=conversation.action, result=str(sleep_time))
                conversation.update()
                out = random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

            else:
                rej.append("rejection")
                out = "잘 못들었습니다." + random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

        if conversation.action == 'Sleep2':
            start = time.time()
            user_in = speech_to_text()  # 완료 시 엔터 입력!
            # user_in = input()
            cw.writerow(['user', user_in])

            answer = nlp.nlp_sleep_answer(user_in=user_in, dic=dic)
            if answer != '':
                sleep_answer = answer
            else:
                response = assistant.message(
                    assistant_id=assistant_info['assistant_id'],
                    session_id=session_id,
                    input={
                        'message_type': 'text',
                        'text': user_in
                    }
                ).get_result()['output']
                sleep_answer = ''
                for i in range(len(response["intents"])):
                    if len(sleep_answer) == 0:
                        if response["intents"][i]["intent"] == '수면의질나쁨' and response["intents"][i]["confidence"] > 0.5:
                            sleep_answer = '나쁨'
                        elif response["intents"][i]["intent"] == '수면의질좋음' and response["intents"][i][
                            "confidence"] > 0.5:
                            sleep_answer = '좋음'

            print("sleep_answer = {}".format(sleep_answer) + '\n')
            print(f'({time.time() - start:.3f}sec)' + '\n')

            if len(sleep_answer) != 0:  # and sleep_answer != 'error':
                conversation.make_slot(slot=slot, action=conversation.action, result=sleep_answer)
                conversation.update()
                out = random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

            else:
                rej.append("rejection")
                out = "잘 못들었습니다." + random.choice(QA_list_Before.before_question_list[conversation.action])
                print(conversation.action, conversation.action_idx)
                print(conversation.user_state)
                print(out + '\n')  # 질문 출력
                tts(out)
                cw.writerow(['msr', out])
                # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=out)

        if conversation.action == 'Bye':
            result = QA_list_Before.before_final_output(slot)
            tts(result)
            # connect.audio_makeplay(tts=text_to_speech, audio_file_name='tts_out.wav', input_text=result)
            print(result)
            conversation.save_text(slot, uid)
            rej_num = len(rej)
            cw.writerow(['rejection', rej_num])
