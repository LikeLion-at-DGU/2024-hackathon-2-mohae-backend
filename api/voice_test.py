import speech_recognition as sr
import pyttsx3
import openai
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

# OpenAI API 키 설정
openai.api_key = os.getenv('OPENAI_API_KEY')

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio, language="ko-KR")
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def get_response_from_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )
    answer = response.choices[0].message['content'].strip()
    return answer

def main():
    print("Choose an input method:")
    print("1. Speak")
    print("2. Type")
    choice = input("Enter 1 or 2: ").strip()

    if choice == '1':
        recognized_text = recognize_speech()
        if recognized_text:
            question = recognized_text
        else:
            print("Speech recognition failed.")
            return
    elif choice == '2':
        question = input("Enter your question: ").strip()
    else:
        print("Invalid choice.")
        return

    if question:
        # OpenAI API에 질문 전송
        answer = get_response_from_openai(question)
        if answer:
            print(f"Answer: {answer}")
            # 응답을 음성으로 출력
            speak_text(answer)
    else:
        print("No question provided.")

if __name__ == "__main__":
    main()
