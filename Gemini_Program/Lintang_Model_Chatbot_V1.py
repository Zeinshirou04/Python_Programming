import os
import google.generativeai as genai
from io import BytesIO
from gtts import gTTS, gTTSError, lang
from playsound import playsound
import socket
import pandas as pd
import csv
from dotenv import load_dotenv

class Chat:
    
    history = []
    
    status = True
    
    chat = None
    
    API_KEY = ''

    def __init__(self):

        try:
            load_dotenv()
            self.API_KEY = os.getenv('API_KEY')
            # print(self.API_KEY) 

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
            model = genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)


            self.loadChat(None)
            self.chat = model.start_chat(history=self.history)
            self.run()
            
        except Exception as er:
            print(f'Error Found: {er}')
        
    
    def speak(self, msg):
        tts = gTTS(msg, lang='id')
        tts.save('Ini.mp3')
        if playsound('Ini.mp3'): return 1
        else: return 0
    
    def saveChat(self, role, text, model):
        
        if model == ('lintang' or 'Lintang' or 2):
            model = None
        
        path = 'Gemini_Program\lintang_chat_history.csv'
        
        # print(f'Choosen model is {model} and the state is {model != None}')
        
        if model != None: 
            path =  'Gemini_Program\history_chat.csv'

        # Tentukan fieldnames (kolom-kolom) untuk header CSV
        fieldnames = ['role', 'text']

        # Tulis data ke dalam file CSV
        with open(path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writerow({'role': role, 'text': text.replace('"', '')})

        # print(f"Data telah disimpan ke {self.csv_filename}")
    
    def message(self, text, model):
        self.saveChat('user', text, model)
        response = self.chat.send_message(text)
        self.saveChat('model', response.text, model)
        self.loadChat(model)
        return response, True
    
    def loadChat(self, model):
        
        if model == ('lintang' or 'Lintang' or 2):
            model = None
        
        path = 'Gemini_Program\lintang_chat_history.csv'
        
        if model != None: 
            path =  'Gemini_Program\history_chat.csv'
        
        # Membaca data dari CSV
        with open(path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            
            # Mengambil setiap baris data
            for row in reader:
                # Menambahkan baris ke dalam list data_from_csv
                self.history.append({
                    'role': row['role'],
                    'parts': [
                        {
                            'text': row['text']
                        }
                    ]
                })
                
    def run(self):
        print("Model Started, Please choose your model: ")
        model = input("1. Wife\n2. Lintang\nModel: ")
        while True:
            text = input('You: ')
            self.status = False
            response, self.status = self.message(text, model)
            self.speak(response.text)
            print(f'Lintang: {response.text}')
        
Chat()