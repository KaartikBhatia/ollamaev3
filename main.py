import pyttsx3
from ollama import Ollama
import socket

engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

ollama = Ollama()

HOST = 'EV3_IP_ADDRESS'  # Replace with your EV3 IP
PORT = 5000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

print("Connected to EV3")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        speak("Goodbye!")
        break

    prompt = f"Control an EV3 robot. Respond with movement commands or text to speak. User said: '{user_input}'"
    response = ollama.chat(prompt).text
    print("Robot says:", response)
    speak(response)

    s.sendall(response.encode('utf-8'))
