# Some Sample code inspired from:
# https://www.youtube.com/watch?v=LTVvHObxc4E

from tkinter import *
from tkcalendar import Calendar
import whisper
import wave
from tkinter import ttk
import torch
import pyaudio
import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pyffmpeg import FFmpeg
import re
import asyncio
import ollama
import pygame
import tkinter as tk
from tkinter import ttk
from threading import Thread
from queue import Queue, Empty
import time
from TTS.api import TTS
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase initialization
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

result_outer = ""
speak_outer = ""
recording = False
audio_queue = Queue(maxsize=1)  # Queue to hold the most recent audio file

splash_root = Tk()
splash_root.title("Splash Screen!!")
splash_root.geometry("300x200")
splash_root.overrideredirect(True)

splash_label = Label(splash_root, text="Splash Screen!", font=("Helvetica", 18))
splash_label.pack(pady=20)

def start_recording():
    global recording, result_outer, speak_outer
    if not recording:
        result_outer = ""
        speak_outer = ""
        recording = True
        print("recording started")
        Thread(target=record).start()

async def convert_from_wav_to_mp3(filename):
    os.system(f"ffmpeg -y -v quiet -i {filename} -ar 16000 -ac 1 -c:a pcm_s16le cleanFile.wav")

def stop_recording():
    global recording
    if recording:
        recording = False
        print("recording stopped")

def on_button_press(event):
    start_recording()

def on_button_release(event):
    stop_recording()

def transcribe_audio(audio):
    model = whisper.load_model("base")  # Change "tiny" to "base" or "small"
    result = model.transcribe(audio, language="en")
    return result["text"].lower()

async def speech_recog(filename):
    global result_outer
    try:
        model = whisper.load_model("tiny")
        audio = whisper.load_audio(filename)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
        options = whisper.DecodingOptions(fp16=False)
        result = whisper.decode(model, mel, options)
        result_no_dots = re.sub(r'\.', '', result.text)
        result_no_dots = result_no_dots.lower()
        print(result_no_dots)
        result_outer = result_no_dots
        root.after(0, update_result_label)
    except Exception as e:
        print(f"Error during speech recognition: {e}")
        result_outer = "Error during speech recognition"
        root.after(0, update_result_label)

def record_audio():
    global recording
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    audio = pyaudio.PyAudio()

    # Get the index of the selected input device
    device_index = None
    for i in range(audio.get_device_count()):
        dev = audio.get_device_info_by_index(i)
        if dev['name'] == selected_input_device.get():
            device_index = i
            break

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, 
                        frames_per_buffer=CHUNK, input_device_index=device_index)
    print("Recording started...")

    frames = []
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)
        
        # Write to a temporary file for real-time transcription
        wf = wave.open("temp_audio.wav", 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    print("Recording stopped.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    audio_queue.put("temp_audio.wav")

def audio_processor():
    while True:
        try:
            filename = audio_queue.get(timeout=1)
            asyncio.run(process_audio(filename))
        except Empty:
            time.sleep(0.1)
        except Exception as e:
            print(f"Error in audio processor: {e}")

async def process_audio(filename):
    await convert_from_wav_to_mp3(filename)
    await speech_recog('cleanFile.wav')
    save_to_firebase()  # Call the Firebase save function
    await speak("Zoe (Premium)")

def record():
    global recording
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    WAVE_OUTPUT_FILENAME = "recordedFile.wav"
    device_index = 2
    audio = pyaudio.PyAudio()

    info = audio.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    index = int(0)
    print("recording via index " + str(index))

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=index, frames_per_buffer=CHUNK)
    print("recording started")
    Recordframes = []

    # Clear the buffer by reading and discarding any existing data
    stream.read(stream.get_read_available())

    while recording:
        data = stream.read(CHUNK)
        Recordframes.append(data)

    print("recording stopped")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(Recordframes))
    waveFile.close()

    # Put the filename in the queue, replacing any existing item
    if not audio_queue.empty():
        try:
            audio_queue.get_nowait()
        except Empty:
            pass
    audio_queue.put(WAVE_OUTPUT_FILENAME)

def update_result_label():
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Recognized: {result_outer}")
    result_text.config(state=tk.DISABLED)

def save_to_firebase():
    global result_outer
    date = "2024-08-29"  # or dynamically get the date
    entry_id = "entry1"  # or dynamically generate the entry ID
    doc_ref = db.collection("journals").document(date).collection("entries").document(entry_id)
    doc_ref.set({
        "text": result_outer,
        "audio_file": "recordedFile.wav",
        "timestamp": firestore.SERVER_TIMESTAMP
    })

async def speak(text):
    # Placeholder for the speak function
    pass

def main_window():
    global result_text
    splash_root.destroy()

    root = Tk()
    root.title('Voice Journal')
    root.geometry("500x500")

    record_button = tk.Button(root, text="Hold to Record")
    record_button.pack(pady=20)

    result_text = tk.Text(root, height=5, wrap=tk.WORD)
    result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    result_text.insert(tk.END, "Recognized: ")
    result_text.config(state=tk.DISABLED)

    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)

    text_info = Text(root, yscrollcommand=scrollbar.set)
    text_info.pack(fill=BOTH)

    scrollbar.config(command=text_info.yview)

    cal = Calendar(root, selectmode='day', year=2024, month=8, day=28)
    cal.pack(pady=20)
    
    record_button.bind('<ButtonPress-1>', on_button_press)
    record_button.bind('<ButtonRelease-1>', on_button_release)

    main_label = Label(root, text="Main Screen", font=("Helvetica", 18))
    main_label.pack()

splash_root.after(3000, main_window)

mainloop()
