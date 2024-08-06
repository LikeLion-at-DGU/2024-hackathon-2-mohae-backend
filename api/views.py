from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile
from .serializers import UserProfileSerializer
import openai
import speech_recognition as sr
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

class AskQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.previous_questions = {}

    def post(self, request, *args, **kwargs):
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

        # 중복 질문 확인
        if question in self.previous_questions:
            return Response({'answer': self.previous_questions[question]}, status=status.HTTP_200_OK)

        # ChatGPT API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message['content'].strip()
        self.previous_questions[question] = answer
        return Response({'answer': answer}, status=status.HTTP_200_OK)
