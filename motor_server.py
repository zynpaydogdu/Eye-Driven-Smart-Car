import socket
import RPi.GPIO as GPIO
from gtts import gTTS
import os
import time
import subprocess

motor1_IN1, motor1_IN2, motor1_IN3, motor1_IN4 = 17, 27, 23, 24
motor1_ENA, motor1_ENB = 22, 25
motor2_IN1, motor2_IN2, motor2_IN3, motor2_IN4 = 5, 6, 13, 19
motor2_ENA, motor2_ENB = 12, 18

all_motor_pins = [
    motor1_IN1, motor1_IN2, motor1_IN3, motor1_IN4, motor1_ENA, motor1_ENB,
    motor2_IN1, motor2_IN2, motor2_IN3, motor2_IN4, motor2_ENA, motor2_ENB
]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in all_motor_pins:
    GPIO.setup(pin, GPIO.OUT)

def move_forward():
    GPIO.output(motor1_ENA, GPIO.HIGH)
    GPIO.output(motor1_ENB, GPIO.HIGH)
    GPIO.output(motor1_IN1, GPIO.HIGH)
    GPIO.output(motor1_IN2, GPIO.LOW)
    GPIO.output(motor1_IN3, GPIO.HIGH)
    GPIO.output(motor1_IN4, GPIO.LOW)
    GPIO.output(motor2_ENA, GPIO.HIGH)
    GPIO.output(motor2_ENB, GPIO.HIGH)
    GPIO.output(motor2_IN1, GPIO.HIGH)
    GPIO.output(motor2_IN2, GPIO.LOW)
    GPIO.output(motor2_IN3, GPIO.HIGH)
    GPIO.output(motor2_IN4, GPIO.LOW)

def turn_right():
    GPIO.output(motor1_ENA, GPIO.HIGH)
    GPIO.output(motor1_ENB, GPIO.HIGH)
    GPIO.output(motor1_IN1, GPIO.HIGH)
    GPIO.output(motor1_IN2, GPIO.LOW)
    GPIO.output(motor1_IN3, GPIO.LOW)
    GPIO.output(motor1_IN4, GPIO.HIGH)
    GPIO.output(motor2_ENA, GPIO.HIGH)
    GPIO.output(motor2_ENB, GPIO.HIGH)
    GPIO.output(motor2_IN1, GPIO.LOW)
    GPIO.output(motor2_IN2, GPIO.HIGH)
    GPIO.output(motor2_IN3, GPIO.HIGH)
    GPIO.output(motor2_IN4, GPIO.LOW)

def turn_left():
    GPIO.output(motor1_ENA, GPIO.HIGH)
    GPIO.output(motor1_ENB, GPIO.HIGH)
    GPIO.output(motor1_IN1, GPIO.LOW)
    GPIO.output(motor1_IN2, GPIO.HIGH)
    GPIO.output(motor1_IN3, GPIO.HIGH)
    GPIO.output(motor1_IN4, GPIO.LOW)
    GPIO.output(motor2_ENA, GPIO.HIGH)
    GPIO.output(motor2_ENB, GPIO.HIGH)
    GPIO.output(motor2_IN1, GPIO.HIGH)
    GPIO.output(motor2_IN2, GPIO.LOW)
    GPIO.output(motor2_IN3, GPIO.LOW)
    GPIO.output(motor2_IN4, GPIO.HIGH)

def stop_motors():
    for pin in all_motor_pins:
        GPIO.output(pin, GPIO.LOW)

def speak(text):
    filename = "komut.mp3"
    if os.path.exists(filename):
        os.remove(filename)
    tts = gTTS(text=text, lang='tr')
    tts.save(filename)
    subprocess.run(["ffplay", "-nodisp", "-autoexit", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(filename)

def handle_command(cmd):
    stop_motors() 
    if cmd == 'sag':
        turn_right()
        speak("Sağa dönüyorum")
    elif cmd == 'sol':
        turn_left()
        speak("Sola dönüyorum")
    elif cmd == 'duz':
        move_forward()
        speak("İleri gidiyorum")
    elif cmd == 'dur':
        stop_motors()
        speak("Duruyorum")
    else:
        speak("Bilinmeyen komut")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 5000)) 
server.listen(1)

print("🚗 Motor sunucusu aktif. Mac'ten komut bekleniyor...")

try:
    while True:
        client, addr = server.accept()
        print(f"🔗 Bağlantı geldi: {addr}")
        data = client.recv(1024).decode().strip()
        print(f"📩 Komut: {data}")
        handle_command(data)
        client.close()
except KeyboardInterrupt:
    print("🛑 Sunucu kapatılıyor...")
finally:
    stop_motors()
    GPIO.cleanup()