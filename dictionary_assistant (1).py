# -*- coding: utf-8 -*-
import pyttsx3
from PyDictionary import PyDictionary
import speech_recognition as sr

class Speaking:

    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()


class ABC:

    def __init__(self):
        self.speaking = Speaking()
        self.dictionary = PyDictionary()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def get_audio_input(self):
        with self.microphone as source:
            self.speaking.speak("Please say the word you want to find the meaning of, sir.")
            print("Listening...")
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query
        except sr.UnknownValueError:
            self.speaking.speak("Sorry, I did not understand that. Could you please repeat?")
            return self.get_audio_input()
        except sr.RequestError:
            self.speaking.speak("Sorry, there seems to be an issue with the speech recognition service.")
            return None

    def Dictionary(self):
        query = self.get_audio_input()
        if query:
            word = self.dictionary.meaning(query)
            if word:
                for part_of_speech in word:
                    meanings = ', '.join(word[part_of_speech])
                    print(f"{part_of_speech}: {meanings}")
                    self.speaking.speak(f"The meanings of {query} as a {part_of_speech} are {meanings}")
            else:
                self.speaking.speak(f"Sorry, I couldn't find the meaning of the word {query}.")
        else:
            self.speaking.speak("Sorry, I couldn't get the word to find the meaning of.")


if __name__ == '__main__':
    assistant = ABC()
    assistant.Dictionary()
