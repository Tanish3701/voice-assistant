
import pyttsx3
import datetime
import speech_recognition as sr
import pyjokes
import weather_forecast as wf
import winshell
import wikipedia
import requests
from random import randint
import wolframalpha
import webbrowser
import subprocess
import json
import operator
import os
from bs4 import BeautifulSoup



engine=pyttsx3.init()
#voice option
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
#voice rate
newVoiceRate=150
engine.setProperty('rate',newVoiceRate)



def speak(audio):
    engine.say(audio)
    engine.runAndWait()



def takeCommand():
        r=sr.Recognizer()
        
        with sr.Microphone() as Source:
            print("listening....")
            r.pause_threshold=1
            audio=r.listen(Source)
        try:
            print("recognizing")
            query=r.recognize_google(audio)
            print(query)
        except Exception as e:
            print(e)
            speak("say that again")
            return "none"
        return query



speak("hello")
speak("this is Pippo")
speak("please tell the password to proceed")
pswrd=takeCommand()




def time():
        Time=datetime.datetime.now().strftime("%I:%M:%S")
        speak("the time is")
        speak(Time)
        print(Time)


#date func
def date():
    year=int(datetime.datetime.now().year)
    month=int(datetime.datetime.now().month)
    day=int(datetime.datetime.now().day)
    speak("the current date is")
    speak(day)
    speak(month)
    speak(year)



def get_operator_fn(op):
    return {
        '+' : operator.add,
        '-' : operator.sub,
        'x' : operator.mul,
        'divided' :operator.__truediv__,
        'Mod' : operator.mod,
        'mod' : operator.mod,
        '^' : operator.xor,
        }[op]

def eval_binary_expr(op1, oper, op2):
    op1,op2 = int(op1), int(op2)
    return get_operator_fn(oper)(op1, op2)


def wishme():
        speak("welcome rachna! Pippo at your service")
        time()
        date()
        hour=int(datetime.datetime.now().strftime("%H"))
        if hour>=0 and hour<12:
            speak("good morning")
        elif hour>=12 and hour<18:
            speak("good afternoon")
        elif hour>=18 and hour<=0:
            speak("good night")




def work(query):
            
            if 'time' in query:
                time()
            elif 'date' in query:
                date()
            elif 'wish' in query:
                wishme()
            elif 'change your name' in query:
                speak("i think my creaters has given me a nice name so i dont want to change it ")
                
            elif "what's your name" in query or "what is your name" in query:
                speak("My Name is Pippo")
                
                print("My friends call me Pippo")
            elif "who made you" in query or "who created you" in query:
                speak("I have been created by rachna Bharti.")
            elif 'joke' in query:
                speak(pyjokes.get_joke())
                
            elif "why were you created" in query:
                speak("because my master rachna has some goals for me. further It's a secret")
            elif "who are you" in query:
                speak("I am virtual assistant.")
            elif 'empty recycle bin' in query:
                winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
                speak("Recycle Bin Recycled")
            elif 'shutdown system' in query:
                speak("Hold On a Sec ! Your system is on its way to shut down")
                subprocess.call('shutdown / p /f')
            elif "where is" in query:
                query = query.replace("where is", "")
                location = query
                speak("User asked to Locate")
                speak(location)
                webbrowser.open("https://www.google.com/maps/place/" + location + "")
            elif "Wikipedia" in query:
                 speak('Searching Wikipedia')
                 query =query.replace("Wikipedia", "")
                 results = wikipedia.summary(query, sentences=3)
                 speak("According to Wikipedia")
                 print(results)
                 speak(results)
            elif 'open YouTube' in query:
                 speak("Here you go to Youtube\n")
                 webbrowser.open("https://www.youtube.com")
            
            
            elif 'search' in query:
                 query = query.replace("search", "")       
                 webbrowser.open("https://www.google.com/search?q="+query+"")
            elif "write a note" in query:
                 speak("What should i write, sir")
                 note = takeCommand()
                 file = open('jarvis.txt', 'w')
                 speak("Sir, Should i include date and time")
                 snfm = takeCommand()
                 if 'yes' in snfm or 'sure' in snfm:
                     strTime = datetime.datetime.now().strftime("%I:%M:%S")
                     file.write(strTime)
                     file.write(" :- ")
                     file.write(note)
                 else:
                     file.write(note)
            elif query == "flip a coin":
                 if randint(1, 2) == 1:
                    speak("It landed on heads!")
                 else:
                    speak("It landed on tails!")
            elif query == "roll a die" or query == "roll a dice":
                 speak("I rolled a " + str(randint(1, 6)))
            elif "show note" in query:
                 speak("Showing Notes")
                 file = open("jarvis.txt", "r")
                 print(file.read())
                 speak(file.read(6))
            elif "news" in query:
                speak("please wait while i am fetching the news for you")
                main_url='https://newsapi.org/v2/top-headlines?country=in&apiKey=4a9c9fe2e7174af7a0f2b56c3f5fac3e'
                main_page=requests.get(main_url).json()
                articles=main_page["articles"]
                head=[]
                day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
                for ar in articles:
                    head.append(ar["title"])
                for i in range (len(day)):
                    print(f"todays {day[i]} news is: ",head[i])
                    speak(f"todays {day[i]} news is: {head[i]}")
            elif "calculate" in query:
                 speak("what do you want to calculate")
                 print(eval_binary_expr(*(takeCommand().split())))
                 speak(eval_binary_expr(*(takeCommand().split())))
            elif "calculation" in query:
                speak("what do you want to calculate")
                question=takeCommand()
                app_id="T4E66K-G9WU9LTG2K"
                client = wolframalpha.Client(app_id)
                res = client.query(question)
                answer = next(res.results).text
                speak("The answer is " + answer)
            elif "weather" in query:
                speak("whice place...")
                plc=takeCommand()
                location=plc
                complete_api_link='https://api.openweathermap.org/data/2.5/weather?q='+location+'&appid=04d7bb4ccab1e569603b955da09f48af'
                api_link=requests.get(complete_api_link)
                api_data=api_link.json()

                if api_data['cod'] =='404':
                     print("invalid city :{},please check your city name".format(location))
                else:
                    temp_city=((api_data['main']['temp'])-273.15)
                    weather_desc=api_data['weather'][0]['description']
                    hmdt=api_data['main']['humidity']
                    wind_spd=api_data['wind']['speed']
                    date_time=datetime.datetime.now().strftime("%d %b %Y | %I:%M:%S %p")
                    print("weather stats for -{} || {}".format(location.upper(),date_time))
                    print("current temp is :{:.2f} deg C".format(temp_city))
                    print("current weather desc :",weather_desc)
                    print("current humidity :",hmdt,'%')
                    print("current wind speed :",wind_spd,'kmph')
    
                    speak("weather stats for -{} || {}".format(location.upper(),date_time))
                    speak("current temp is :{:.2f} degree Celsius".format(temp_city))
                    speak("current weather description is  :"+weather_desc)
                    speak(f"current humidity :{hmdt} %")
                    speak(f"current wind speed {wind_spd} kmph")
                 
        
            elif "do nothing" in query:
                speak("Thanks for giving me your time")
                quit()
            

if "python" in pswrd:
  wishme()
  while True:
    userInput = input("Would you like me to listen? (y/n)\n")
    if userInput == "y":
        speak("how can i help you")
        work(takeCommand())
    if userInput == "n":
        speak("thanks for giving me your time")
        quit()
else:
    speak("wrong password")
    quit()
