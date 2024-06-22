import os
import google.generativeai as genai
from io import BytesIO
from gtts import gTTS, gTTSError, lang
from playsound import playsound
import socket
import pandas as pd
import csv

class Chat:
    
    csv_filename = 'history_chat.csv'
    
    history = []
    
    status = True
    
    chat = None
    
    def __init__(self):
        try:
            genai.configure(api_key=os.environ['API_KEY'])
            model = genai.GenerativeModel('gemini-1.5-flash')
            self.loadChat()
            # print(self.history)
            self.chat = model.start_chat(history=self.history)
            self.run(self.history)
        except:
            os.environ['API_KEY'] = 'YOUR_API_KEY'
            genai.configure(api_key=os.environ['API_KEY'])
            model = genai.GenerativeModel('gemini-1.5-flash')
            self.loadChat()
            self.chat = model.start_chat(history=self.history)
            self.run()
    
    def speak(msg):
        tts = gTTS(msg, lang='id')
        tts.save('Ini.mp3')
        playsound('Ini.mp3')
        return 1
    
    def saveChat(self, role, text):

        # Tentukan fieldnames (kolom-kolom) untuk header CSV
        fieldnames = ['role', 'text']

        # Tulis data ke dalam file CSV
        with open(self.csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            writer.writerow({'role': role, 'text': text.replace('"', '')})

        print(f"Data telah disimpan ke {self.csv_filename}")
    
    def message(self, text):
        self.saveChat('user', text)
        response = self.chat.send_message(text)
        self.saveChat('model', response.text)
        self.loadChat()
        return response, True
    
    def loadChat(self):
        # Membaca data dari CSV
        with open(self.csv_filename, 'r', encoding='utf-8') as csvfile:
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
        while True:
            text = input()
            self.status = False
            response, self.status = self.message(text)
            print(response.text)
        
Chat()