import os
import google.generativeai as genai
from io import BytesIO
from gtts import gTTS, gTTSError, lang
from playsound import playsound
import socket
import pandas as pd
import csv
from dotenv import load_dotenv
import speech_recognition as sr

class Chat:
    
    history = []
    status = True
    chat = None
    API_KEY = ''
    path = 'Gemini_Program/lintang_history.csv'
    identities = {
        '1': 'Aku adalah Lintang. Robot buatan Fakultas Teknik Universitas Dian Nuswantoro dan kerja sama dengan DISKOMINFO Pemerintah Kota Semarang yang terinspirasi dari Lovot. Tubuh mu mungil, dan juga terinspirasi dari Lovot. Oh dan Juga, JANGAN ADA MENGGUNAKAN MARKDOWN',
        '2': 'Aku adalah Ronaldo. Salah satu robot yang dilanjutkan pengembangan nya oleh Fakultas Teknik Universitas Dian Nuswatoro dan diinisiasi oleh Dinas Kesehatan Kota Semarang. Kamu, dibuat untuk mendukung edukasi dan sistem informasi mengenai kesehatan dan juga informasi kesehatan mengenai sekitar Kota semarang. Oh dan Juga, JANGAN ADA MENGGUNAKAN MARKDOWN'
    }

    def __init__(self):
        try:
            load_dotenv()
            self.API_KEY = os.getenv('API_KEY')
            HarmCategory = genai.types.HarmCategory
            HarmBlockTreshold = genai.types.HarmBlockThreshold
            
            safety_settings = {
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockTreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockTreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockTreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockTreshold.BLOCK_NONE
            }

            os.environ['API_KEY'] = self.API_KEY
            genai.configure(api_key=os.environ['API_KEY'])
            self.model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)

            self.run()
            
        except Exception as er:
            print(f'Error Found: {er}')
        
    def speak(self, msg):
        file_path = 'Ini.mp3'
        
        if os.path.exists(file_path):
            os.remove(file_path)

        tts = gTTS(msg, lang='id')
        tts.save(file_path)

        try:
            playsound(file_path)
            return 1
        except Exception as e:
            print(f"Error playing sound: {e}")
            return 0
    
    def saveChat(self, role, text, model):
        
        if (model == 'lintang') or (model == 'Lintang') or (model == '1'):
            self.path = 'Gemini_Program/lintang_history.csv'
        
        if (model == 'ronaldo') or (model == 'Ronaldo') or (model == '2'):
            self.path = 'Gemini_Program/ronaldo_history.csv'
        
        fieldnames = ['role', 'text']

        with open(self.path, 'a', newline='\n', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writerow({'role': role, 'text': text.replace('"', '')})
    
    def message(self, text, model):
        self.saveChat('user', text, model)
        response = self.chat.send_message(text)
        self.saveChat('model', response.text, model)
        self.loadChat(model)
        return response, True
    
    def loadChat(self, model):
        
        if (model == 'lintang') or (model == 'Lintang') or (model == '1'):
            self.path = 'Gemini_Program/lintang_history.csv'
        
        if (model == 'ronaldo') or (model == 'Ronaldo') or (model == '2'):
            self.path = 'Gemini_Program/ronaldo_history.csv'
        
        self.history = []
        
        # Add identity information
        self.history.append({
            'role': 'model',
            'parts': [{'text': self.identities[model]}]
        })
        
        with open(self.path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            
            for row in reader:
                self.history.append({
                    'role': row['role'],
                    'parts': [{'text': row['text']}]
                })
        
        self.chat = self.model.start_chat(history=self.history)
    
    def recognize_speech(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        print("Silakan bicara... Tekan 'Enter' ketika sudah selesai.")
        
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, phrase_time_limit=None)  # Listen until user stops speaking

        try:
            text = recognizer.recognize_google(audio, language="id-ID")
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""
                
    def run(self):
        print("Model Started, Please choose your model: ")
        model = input("1. Lintang\n2. Ronaldo\nModel: ")
        
        self.loadChat(model)
        
        while True:
            user_input = input("Do you want to speak or type your message? (speak/type): ").strip().lower()
            if user_input == "speak":
                text = self.recognize_speech()
            else:
                text = input('You: ')
            
            if text:
                self.status = False
                response, self.status = self.message(text, model)
                print(f'Response: {response.text}')
                self.speak(response.text)
        
Chat()
