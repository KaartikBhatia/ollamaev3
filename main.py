import socket
import json
import pyttsx3
from ollama import Ollama


def load_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)

memory = load_memory()

engine = pyttsx3.init()

def speak(text):
    print("Robot:", text)
    engine.say(text)
    engine.runAndWait()


ollama = Ollama()

EV3_IP = "192.168.1.XX"  # CHANGE THIS
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((EV3_IP, PORT))

print("Connected to EV3")


while True:

    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        speak("Shutting down.")
        break

    if "remember that" in user_input.lower():
        fact = user_input.lower().replace("remember that", "").strip()
        memory[fact] = True
        save_memory(memory)
        speak("I will remember that.")
        continue

    if "what do you remember" in user_input.lower():
        if memory:
            memories = ", ".join(memory.keys())
            speak("I remember: " + memories)
        else:
            speak("I do not remember anything yet.")
        continue

    if "start autonomous mode" in user_input.lower():
        sock.sendall(b"auto mode")
        speak("Autonomous mode activated.")
        continue

    if "stop autonomous mode" in user_input.lower():
        sock.sendall(b"remote mode")
        speak("Returning to remote control mode.")
        continue

    prompt = f"""
You are an EV3 robot assistant.
You can:
- Move forward
- Move backward
- Turn left
- Turn right
- Stop

Respond naturally but include movement words if needed.
User said: {user_input}
"""

    response = ollama.chat(prompt).text

    speak(response)

    sock.sendall(response.encode("utf-8"))
