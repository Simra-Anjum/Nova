import speech_recognition as sr 
import pyttsx3
import webbrowser
import datetime
import requests
import yt_dlp
from dotenv import load_dotenv
import os
from google import genai
load_dotenv()
newsapi= os.getenv("NEWS_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)
recognizer = sr.Recognizer()
# engine = pyttsx3.init()


def speak(message):
    engine = pyttsx3.init("sapi5")
    engine.say(message)
    engine.runAndWait()

def test_gemini():
    response = client.interactions.create(
        model="gemini-3.8-flash",
        input="Explain Python in one simple sentence."
    )
    print(response.output_text) 

def process_command(command):
    if "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "search" in command:
        search_query = command.replace("search", "").strip()
        webbrowser.open("https://www.google.com/search?q=" + search_query)
   
    elif "wikipedia" in command:
        topic = command.replace("wikipedia", "").strip()

        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + topic.replace(" ", "_")

        headers = {
        "User-Agent": "JarvisPythonProject/1.0"
         }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            speak(data["extract"])
        else:
            speak("Sorry, I could not find information about that.")
         
    elif "time" in command:
         current_time = datetime.datetime.now().strftime("%I:%M %p")
         print(current_time)
         speak(f"The time is {current_time}")
    elif command.startswith("play "):
        song = command.replace("play ", "", 1).strip()
        ydl_options = {
            "quiet" : True,
            "no-warnings" : True,
            "extract_flat" : True,
            "default_search" : "ytsearch1"
            }
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            result = ydl.extract_info("ytsearch1:" + song, download=False)

       
        if result and result.get("entries"): 
            video = result["entries"][0]
            video_url = "https://www.youtube.com/watch?v=" + video["id"] + "&autoplay=1"
            webbrowser.open(video_url)  
        else:
            speak("Sorry, I could not find that song.")         
        
    elif "instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
    elif "facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
    elif "linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://www.linkedin.com")
    elif "news" in command:
        
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        response = requests.get(url)
        

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            print("Total articles:", len(articles))
            if not articles:
                speak("No news articles found.")
            else:
                for article in articles[:5]:
                    title = article.get("title")
                    if title:
                        print(title)
                        speak(title)
        else:
            speak("Sorry, I could not fetch the news.")
   
    elif "ai" in command:
        question = command.replace("ask ai", "", 1).strip()

        if not question:
            speak("Please tell me what you want to ask.")
            return

        try:
            response = client.interactions.create(
                model="gemini-3.8-flash",
                input=question
            )

            answer = response.output_text
            print("Jarvis:", answer)
            speak(answer)

        except Exception as e:
            print("Gemini error:", e)
            speak("Sorry, AI is temporarily unavailable.")
    elif "exit" in command:
        speak("Goodbye!")
        return "exit"
    elif "shutdown" in command:
        speak("Shutting down Nova.")
        return "shutdown" 
    else:
        speak("Sorry, I did not understand that command.")            
                 
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print("you said:", command)
        return command.lower()

    except sr.UnknownValueError:
        print("Sorry, I could not understand.")
        speak("Sorry, I could not understand.")
        return ""
    except sr.RequestError:
        print("Speech service is unavailable.")
        return ""
    except Exception as e:
        print("Error:", e)
        return             

speak("Initializing Nova.....") 
while True:
    command = listen()
    if "nova" in command:
        speak("Yes?")
        while True:
            command = listen()
            if not command:
                continue
            result=process_command(command)
            if result == "exit":
                break
            elif result == "shutdown":
               speak("Goodbye!")
               raise SystemExit 
    elif "shutdown" in command:
        speak("Goodbye!")
        raise SystemExit           
      