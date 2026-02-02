import speech_recognition as sr

def listen():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Listening...")
            
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source)
            text = r.recognize_google(audio)
            text = text.lower()  
            return text

    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        return "error"

    except sr.UnknownValueError:
        print("Could not understand audio")
        return "error"

    except KeyboardInterrupt:
        print("Program terminated by user")
        return "error"
    
print(listen())