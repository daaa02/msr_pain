from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.text_to_speech_v1 import TextToSpeechV1
from pygame import mixer
import os
import time
import requests

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

HIGH = 1
LOW = 0


def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Connection:
    def __init__(self):
        # speech to text variants
        self.kakao_account = 'f8f8c3f66bb3310016fdeccffba152e8'
        os.system(f'gpio mode 7 out;gpio write 7 {HIGH}')

        self.STREAMING_LIMIT = 240000  # 4 minutes
        self.SAMPLE_RATE = 16000
        self.CHUNK_SIZE = int(self.SAMPLE_RATE / 10)  # 100ms

        self.RED = '\033[0;31m'
        self.GREEN = '\033[0;32m'
        self.YELLOW = '\033[0;33m'

        self.user_words = ''

    def assistant_connect(self, assistant_id):
        assistant_info = {
            'apikey': 'wSyvgsNL1br9lTSE9ri_34HG0gbc3qp7v7dpcGhOr70f',
            'version': '2020-07-02',
            'url': ' https://api.kr-seo.assistant.watson.cloud.ibm.com/instances/4d8c94cd-12be-4ae5-8fd1-f955720862a1',
            'assistant_id': assistant_id
        }

        authenticator = IAMAuthenticator(assistant_info['apikey'])
        assistant = AssistantV2(
            version=assistant_info['version'],
            authenticator=authenticator
        )

        assistant.set_service_url(assistant_info['url'])

        response = assistant.create_session(
            assistant_id=assistant_info['assistant_id'],

        ).get_result()

        session_id = response['session_id']
        return assistant, assistant_info, session_id

    def tts_connect(self):
        tts_info = {
            # dyk98498@gmail.com
            "url": "https://api.kr-seo.text-to-speech.watson.cloud.ibm.com/instances/39455eb0-512a-4b7d-b0c5-e6adc97f0ef9",
            "apikey": "fCZb_a0tm59A4oYpyolYCn2sJ6PM2FPVOTZaMMQQ3j5c",

            # # dyk984@daum.net
            # "url": "https://api.kr-seo.text-to-speech.watson.cloud.ibm.com/instances/463f76da-a286-43b3-a645-feefc2b922c6",
            # "apikey": "8ynSNM7tM1q6Y4OquVPyIyAaYr6_GcbVLVVybUBaW2os",
        }
        authenticator = IAMAuthenticator(tts_info['apikey'])
        tts = TextToSpeechV1(
            authenticator=authenticator
        )
        tts.set_service_url(tts_info['url'])

        return tts

    def audio_makeplay(self, tts, audio_file_name, input_text):  # , sleep_time = 6):
        # tts 로봇 음성 오디오파일로 저장
        with open(audio_file_name, 'wb') as audio_file:
            audio_file.write(
                tts.synthesize(
                    text=input_text,
                    accept='audio/wav',
                    voice='ko-KR_YunaVoice'  # -GB_KateVoice' #'Yuna'
                ).get_result().content
            )

        # 로봇 음성 오디오파일 재생
        freq = 16000
        bitsize = -16
        channels = 1
        buffer = 2048
        mixer.init()
        # mixer.init(freq, bitsize, channels, buffer)
        q = mixer.Sound(audio_file_name)
        q.play()
        while mixer.get_busy() == True:
            time.sleep(1.0)
        # print(len(input_text))

    # kakao tts api
    def tts(self, string, filename="tts.wav"):

        if self.kakao_account in [None, '']:
            raise Exception('Kakao account invalid')

        url = "https://kakaoi-newtone-openapi.kakao.com/v1/synthesize"
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': 'KakaoAK ' + self.kakao_account
        }
        r = requests.post(url, headers=headers, data=string.encode('utf-8'))
        with open(filename, 'wb') as f:
            f.write(r.content)

    # kakao tts play
    def play(self, filename, out='local', volume='-2000.0', background=True):

        if not os.path.isfile(filename):
            raise Exception(f'"{filename}" does not exist')

        if not filename.split('.')[-1] in ['mp3', 'wav']:
            raise Exception(f'"{filename}" must be (mp3|wav)')

        if not out in ['local', 'hdmi', 'both']:
            raise Exception(f'"{out}" must be (local|hdmi|both)')

        if not isNumber(volume):
            raise Exception(f'"{volume}" is not Number')

        if type(background) != bool:
            raise Exception(f'"{background}" is not bool')

        opt = '&' if background else ''
        os.system(f'omxplayer -o {out} --vol {volume} {filename} {opt}')
