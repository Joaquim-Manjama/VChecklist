import time

def getTime():
    return f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}]"

def log(message):
    f = open("files/Log.txt", "a")
    f.write(f"{getTime()} - {message}\n")
    f.close()

def separate():
    f = open("files/Log.txt", "a")
    f.write("\n" + "-"*50 + "\n\n")
    f.close()