from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.text_to_speech_v1 import TextToSpeechV1
from pygame import mixer
import time

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class Connection:
    def __init__(self):
        # speech to text variants
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
        mixer.init(freq, bitsize, channels, buffer)
        mixer.Sound(audio_file_name).play()
        while mixer.get_busy() == True:
            time.sleep(1.0)
        # print(len(input_text))
