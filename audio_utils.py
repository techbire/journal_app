import pyaudio
import wave
from queue import Queue, Empty
import os
import asyncio

# Function to record audio
def record_audio(queue, recording_event):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    print("Recording started...")

    frames = []
    while recording_event.is_set():
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording stopped.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    filename = "temp_audio.wav"
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    queue.put(filename)

# Function to convert WAV to MP3 (or other formats)
async def convert_wav_to_mp3(filename):
    output_filename = "cleanFile.wav"
    os.system(f"ffmpeg -y -v quiet -i {filename} -ar 16000 -ac 1 -c:a pcm_s16le {output_filename}")
    return output_filename
