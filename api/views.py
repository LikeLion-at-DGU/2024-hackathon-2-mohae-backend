from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile
from .serializers import UserProfileSerializer
import openai
import speech_recognition as sr
from django.conf import settings
import random

openai.api_key = settings.OPENAI_API_KEY

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

class AskQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    fixed_answers = {
        "button1": "모해는 부모님과 자녀 간의 소통을 촉진하고, 서로의 삶을 더 잘 이해하고 지원할 수 있도록 돕는 혁신적인 웹 서비스입니다. 이와 더불어 부모님 세대의 건강을 간접적으로 자녀가 챙기고, 부모님 스스로도 자신의 건강과 교육을 챙길 수 있습니다.",
        "button2": "부모님과 함께 할 수 있는 활동으로는 산책, 요리, 영화 감상, 또는 근처 공원에서 피크닉을 추천드립니다. 또한, 모해의 문화생활 페이지에서 부모님과 함께 참여할 수 있는 지역 행사나 전시회를 찾아보세요.",
        "button3": "모해의 건강 챌린지 기능은 사용자가 건강 목표를 설정하고 달성할 수 있도록 돕는 기능입니다. 챌린지를 시작하려면 메인 페이지에서 '건강' 섹션으로 이동하여 원하는 챌린지를 선택하세요.",
        "button4": "가족과 함께 즐길 수 있는 활동으로는 가족 게임, 공동 요리 시간, 야외 캠핑, 또는 가족 사진첩 만들기 등이 있습니다. 모해의 일정 캘린더를 사용하여 가족 이벤트를 계획해 보세요.",
        "button5": "가족 사진첩을 만들려면 모해의 사진첩 기능으로 이동한 후 '새 앨범 만들기'를 선택하세요. 가족과 함께 찍은 사진을 업로드하고, 특별한 추억을 공유해 보세요.",
        "button6": "부모님과 함께할 수 있는 문화생활 활동으로는 미술 전시회, 음악회, 연극 관람 등이 있습니다. 모해의 문화생활 페이지에서 가까운 행사 정보를 확인해 보세요.",
        "button7": "가족 모임을 계획하려면 모해의 일정 캘린더 기능을 사용해 보세요. 일정에 가족 모임을 추가하고, 가족 구성원들을 일정에 추가할 수 있습니다.",
        "button8": "부모님과 함께 운동하려면 모해의 건강 챌린지 섹션에서 가벼운 산책, 요가, 또는 스트레칭 루틴을 선택해 함께 운동을 시작해 보세요.",
        "button9": "가족과 함께 할 수 있는 건강 챌린지로는 '운동장 한바퀴 뛰기', '매일 물 2리터 마시기' 등이 있습니다. 가족 모두 함께 참여하여 건강한 생활을 유지해 보세요.",
        "button10": "부모님을 위한 특별한 이벤트로는 깜짝 가족 모임, 부모님과 함께하는 추억 여행, 또는 부모님께 감사의 편지 쓰기를 추천합니다. 모해의 일정 캘린더에 이벤트를 기록해 보세요.",
    }

    def post(self, request, *args, **kwargs):
        if 'button_id' in request.data:
            button_id = request.data.get('button_id')
            if button_id in self.fixed_answers:
                return Response({'answer': self.fixed_answers[button_id]}, status=status.HTTP_200_OK)
            else:
                return Response({'error': "Invalid button_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        recognizer = sr.Recognizer()
        question = request.data.get('question', '')

        if 'audio' in request.FILES:
            audio_file = request.FILES['audio']
            with sr.AudioFile(audio_file) as source:
                audio = recognizer.record(source)
                try:
                    question = recognizer.recognize_google(audio, language="ko-KR")
                except sr.UnknownValueError:
                    return Response({'error': "Could not understand audio"}, status=status.HTTP_400_BAD_REQUEST)
                except sr.RequestError as e:
                    return Response({'error': f"Could not request results from Google Speech Recognition service; {e}"}, status=status.HTTP_400_BAD_REQUEST)
        elif not question:
            return Response({'error': "No question or audio provided"}, status=status.HTTP_400_BAD_REQUEST)

        # 고정 질문 확인
        if question in self.fixed_answers:
            return Response({'answer': self.fixed_answers[question]}, status=status.HTTP_200_OK)

        # 중복 질문 확인
        if question in self.previous_questions:
            return Response({'answer': self.previous_questions[question]}, status=status.HTTP_200_OK)

        # ChatGPT API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly assistant who talks in a warm and family-like manner."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message['content'].strip()
        self.previous_questions[question] = answer
        return Response({'answer': answer}, status=status.HTTP_200_OK)

class RandomQuestionsView(AskQuestionView):

    def get(self, request, *args, **kwargs):
        all_buttons = list(self.fixed_answers.keys())
        random_buttons = random.sample(all_buttons, 3)
        random_questions = {key: self.fixed_answers[key] for key in random_buttons}
        return Response(random_questions, status=status.HTTP_200_OK)
