from konlpy.tag import Kkma
from konlpy.tag import Komoran
from konlpy.tag import Okt
from pandas import DataFrame, Series
import pandas as pd


class NLP():
    def __init__(self):
        self.kk = Kkma()
        self.km = Komoran()
        self.okt = Okt()
        self.user_tag = []
        self.temp = {}
        self.n = 0

    def nlp_position(self, user_in, dic):
        # flatten : True는 1차원 list, False는 2차원 list( 띄어쓰기에 따라 []에 넣는지 마는지 차이
        # join은 True 시 ('허리/NNG')처럼 한 요소로 출력 False는 ('허리','NNG')

        self.user_tag = self.okt.pos(user_in)  # self.km(user_in,flatten=True)
        self.temp.clear()
        # print(self.user_tag)

        position = ""
        user_painpoint = []
        tmp = []
        tmp2 = []

        for i in range(len(self.user_tag)):
            if self.user_tag[i][1].startswith('N'):
                tmp.append(str(self.user_tag[i][0]))
        tmp = list(set(tmp))
        # print("user_painpoint = ", tmp)
        keys = list(dic.Position.keys())
        values = list(dic.Position.values())

        for i in range(len(tmp)):
            for j in range(len(keys)):
                for k in range(len(values[j])):
                    if tmp[i] == values[j][k] and self.temp.get(keys[j]) == None:
                        self.temp[keys[j]] = [tmp[i]]
                    elif tmp[i] == values[j][k] and self.temp.get(keys[j]) != None:
                        self.temp.get(keys[j]).append(tmp[i])  # self.temp[keys[j]] =
        # 한 신체부위에 여러 값이 들어와 있을 때 신체부위 키(ex)다리)와 같은 값이 들어와 있을 경우(value: 다리, 허벅지양쪽)
        # 세부적인 것만 남기는 역할(환자가 같은 부위를 여러 어휘로 말한 경우 처리)
        # ex) {다리 : ['다리','허벅지']} -> {다리: '허벅지'}
        # print("temp = ", self.temp)
        p1 = None
        for point, val in self.temp.items():
            # print("point = ", point, ", val = ", val)
            p1 = bool([True for i in range(len(val)) if len(val) > 1 and point == val[i]])
            if p1 == True:
                val.remove(point)
            # print("p1 = ", p1, " val = ", val)
            p1 = None
            if len(val) == 1:
                self.temp[point] = ''.join(val)  # list->문자열로 변환
        val = self.temp.values()
        for i in val:
            user_painpoint.append(i)
        return user_painpoint
        #
        #     #     position += self.user_tag[i][0]
        #     # elif position != '':
        #     #     user_painpoint.append(position)
        #     #     position = ''
        #
        # keys = list(dic.Position.keys())
        # values = list(dic.Position.values())
        #
        # for i in range(len(user_painpoint)):                          #user_painpoint =['왼쪽허리','어깨','다리','허벅지양쪽']
        #     for j in range(len(keys)):
        #         for k in range(len(values[j])):
        #             # user_painpoint에서 사전에 해당되는 단어부분이 있는지 찾고(ex)왼쪽허리 - 허리), 결과를 저장할 temp에 허리에 해당하는 단어가 들어왔는지 확인
        #             if user_painpoint[i].find(values[j][k]) != -1 and self.temp.get(keys[j]) == None:
        #                 self.temp[keys[j]] = user_painpoint[i]              #해당하는 단어가 안들어 와있을 경우 문자열형태로 값 추가
        #             elif user_painpoint[i].find(values[j][k]) != -1 and self.temp.get(keys[j]) != None:
        #                 self.temp[keys[j]] = [self.temp.get(keys[j]), user_painpoint[i]]     #해당하는 단어가 있을 경우('허벅지양쪽'이 처리될 때 이미 '다리'가 들어와있음) list형태로 만들어서 추가
        #
        # # 한 신체부위에 여러 값이 들어와 있을 때 신체부위 키(ex)다리)와 같은 값이 들어와 있을 경우(value: 다리, 허벅지양쪽)
        # # 세부적인 것만 남기는 역할(환자가 같은 부위를 여러 어휘로 말한 경우 처리)
        # # ex) {다리 : ['다리','허벅지양쪽']} -> {다리: '허벅지양쪽'}
        # for point, val in self.temp.items():
        #     if type(val) == list and val.index(point) != ValueError:
        #         val.remove(point)
        #         print(len(val))
        #         if len(val) == 1:
        #             self.temp[point] = ''.join(val)
        #             user_painpoint.remove(point)
        #
        # print("temp \n{}".format(self.temp))
        # return user_painpoint

    def nlp_YesOrNo(self, user_in, dic):
        answer = ''
        for i in range(len(dic.YesorNo['Yes'])):
            if dic.YesorNo['Yes'][i] in user_in:
                answer = '있음'  # 'Yes'
        for j in range(len(dic.YesorNo['No'])):
            if dic.YesorNo['No'][j] in user_in:
                answer = '없음'  # 'No'
        return answer

    def nlp(self, user_in):
        # print(self.kk.pos(user_in))
        # print(self.km.pos(user_in))
        print(self.okt.pos(user_in))

    def nlp_sleep_time(self, user_in, dic):
        sleep_time = -1
        ko = -1
        nb = -1
        for i, j in enumerate(dic.sleep_time):
            x = user_in.find(j)
            if x != -1:
                ko = i
                # sleep_time = i
        for i, j in enumerate(dic.sleep_time_number):  # range(len(
            x = user_in.find(j)
            if x != -1:
                nb = i
        sleep_time = max(ko, nb)
        return sleep_time

    def nlp_bedtime(self, user_in, dic):
        bedtime = -1
        ko = -1
        nb = -1
        for i, j in enumerate(dic.sleep_time):
            x = user_in.find(j)
            if x != -1:
                ko = i
                # sleep_time = i
        for i, j in enumerate(dic.sleep_time_number):  # range(len(
            x = user_in.find(j)
            if x != -1:
                nb = i
        bedtime = max(ko, nb)
        return bedtime

    def nlp_asleep_time(self, user_in, dic):
        asleep_time = -1
        ko = -1
        nb = -1
        for i, j in enumerate(dic.asleep_time):
            x = user_in.find(j)
            if x != -1:
                ko = i
                # sleep_time = i
        for i, j in enumerate(dic.asleep_time_number):  # range(len(
            x = user_in.find(j)
            if x != -1:
                nb = i
        asleep_time = max(ko, nb)
        return asleep_time

    def nlp_sleep_answer(self, user_in, dic):
        x = []
        answer = ''
        in_okt = self.okt.pos(user_in)
        if len(in_okt) < 5:
            for n in range(len(in_okt)):
                if in_okt[n][0] in dic.YesorNo["Yes"]:
                    x.append(1)
                if in_okt[n][0] in dic.YesorNo["No"]:
                    x.append(0)
            if 0 in x and 1 in x:
                answer = 'error'
            elif 1 in x and 0 not in x:
                answer = '좋음'
            elif 0 in x and 1 not in x:
                answer = '나쁨'
        return answer

    def nlp_severity(self, user_in, dic):
        x = []
        severity = []
        if any(chr.isdigit() for chr in user_in):
            for i in dic.severity_number:
                x = user_in.find(i)
                if x != -1:
                    severity.append(i)
        else:
            for i in range(len(dic.severity_word)):
                if dic.severity_word[i] in user_in:
                    severity.append(i)
        return severity

    # def make_slot(self, points):   # ID 받는거 추가해야함, 통증 부위 개수에 따라 slot 만드는 함수
    #     before_slot_list = []
    #     # for point in points:
    #     #     dic_tmp = {'ID': 0, 'Position' : point}
    #     #     before_slot_list.append(dic_tmp)
    #     return before_slot_list

    # def slot_add(self,slot, add_val):      # slot에 값 추가 함수


class Dictionary():
    def __init__(self):
        self.prefix_dir = ['왼', '오른', '중간', '가운데', '양' '앞', '뒤', '뒷', '옆', '위', '윗', '아래', '아랫', '쪽', '면', '번째', '사이',
                           '부근', '안', '밖']
        self.Position = {'눈': ['눈', '눈가', '눈밑', '눈썹', '속눈썹', '눈동자', '눈알', '흰자', '검은자', '각막', '눈꺼풀'],
                         '코': ['코', '콧볼', '콧구멍', '콧대', '콧등', '비강'],
                         '입': ['입', '입술', '이', '치아', '앞니', '윗니', '아랫니', '어금니', '사랑니', '송곳니', '잇몸', '혀', '혓바닥', '입천장',
                               '침샘', '구강'],
                         '귀': ['귀', '귓구멍', '귓불', '달팽이관', '고막', '귓바퀴', '전정기관'],
                         '턱': ['턱', '턱뼈', '턱관절'],
                         '볼': ['턱', '턱뼈', '턱관절'],
                         '얼굴': ['얼굴', '이마', '미간', '인중'],
                         '머리': ['머리', '관자놀이', '뒷골'],
                         '목': ['목', '목덜미', '목구멍', '목젖', '식도', '기도', '인두', '편도'],
                         '팔': ['팔', '팔목', '팔꿈치'],
                         '어깨': ['어깨', '승모', '겨드랑이'],
                         '손': ['손', '손목', '손등', '손바닥', '손톱', '손가락', '엄지', '검지', '중지', '약지'],
                         '가슴': ['가슴', '명치', '갈비뼈', '간', '폐', '콩팥', '신장', '흉강', '쓸개', '담낭'],
                         '배': ['배', '배꼽', '속', '위', '장', '대장', '소장', '맹장', '십이지장', '췌장', '허파'],
                         '허리': ['허리', '옆구리'],
                         '등': ['등', '날갯죽지', '날개죽지', '척추'],
                         '생식기': ['생식기', '난소', '자궁', '항문'],
                         '다리': ['다리', '허벅지', '종아리', '넓적다리', '허벅다리', '장딴지', '정강이'],
                         '무릎': ['무릎'],
                         '엉덩이': ['엉덩이', '골반', '엉치', '고관절', '둔부'],
                         '발': ['발', '발목', '발등', '발꿈치', '뒷꿈치', '복사뼈', '복숭아뼈', '발가락', '발톱', '아킬레스건', '발바닥']
                         }

        self.YesorNo = {'Yes': ['네', '예', '응', '어', '맞아요', '맞아', '그래', '그렇습니다', '맞습니다', '맞어'],
                        'No': ['아니', '아니오', '아니요', '안', '아뇨', '아닌', '아닙니다', '아냐', '아닐', '별로', '글쎄', '그다지', '딱히', '없습니다',
                               '없어', '없네', '없는', '없다', '없고', '없음', '없으예', '없소']}

        self.sleep_time = ['영', '한', '두', '세', '네', '다섯', '여섯', '일곱', '여덟', '아홉', '열', '열한', '열두', '열세',
                           '열네', '열다섯', '열여섯', '열일곱', '열여덟', '열아홉', '스무', '스물하나', '스물두',
                           '스물세', '스물네']
        self.sleep_time_number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
                                  '16', '17', '18', '19', '20', '21', '22', '23', '24']

        self.asleep_time = ['일', '이', '삼', '사', '오', '육', '칠', '팔', '구', '십', '십오', '이십', '이십오', '삼십', '삼십오',
                            '사십', '사십오', '오십']
        self.asleep_time_number = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '15', '20', '25', '30', '35',
                                   '40', '45', '50']

        self.severity_number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.severity_word = ['영', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구', '십']
