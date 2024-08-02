from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import openai
import speech_recognition as sr
from django.conf import settings

# OpenAI API 키 설정
openai.api_key = settings.OPENAI_API_KEY

class AskQuestionView(APIView):
    permission_classes = [AllowAny]

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

        # ChatGPT API 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message['content'].strip()
        return Response({'answer': answer}, status=status.HTTP_200_OK)
