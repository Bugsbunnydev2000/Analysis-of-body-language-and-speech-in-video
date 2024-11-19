import os
from moviepy.editor import VideoFileClip
import whisper
import json
import google.generativeai as genai

# Configure the Gemini API key
GOOGLE_API_KEY = 'Your-key'
genai.configure(api_key=GOOGLE_API_KEY)

# Paths
video_file_path = "Your-path"
audio_dir = "Your-path"
stt_dir = "Your-path"
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(stt_dir, exist_ok=True)

# Step 1: Convert video to audio (MP3)
audio_file_path = os.path.join(audio_dir, "Test-1.mp3")
print("Converting video to audio...")
video_clip = VideoFileClip(video_file_path)
video_clip.audio.write_audiofile(audio_file_path)
video_clip.close()
print(f"Audio saved at {audio_file_path}")

# Step 2: Transcribe audio using the local Whisper model
print("Transcribing audio locally with Whisper...")
whisper_model = whisper.load_model("base")  # You can use "tiny", "base", "small", "medium", "large"
transcription_result = whisper_model.transcribe(audio_file_path)

# Extract the transcription text
transcription_text = transcription_result['text']

# Save transcription as TXT and JSON
stt_txt_path = os.path.join(stt_dir, "Test-1.txt")
stt_json_path = os.path.join(stt_dir, "Test-1.json")

with open(stt_txt_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(transcription_text)

with open(stt_json_path, 'w', encoding='utf-8') as json_file:
    json.dump({'transcription': transcription_text}, json_file, ensure_ascii=False, indent=4)

print(f"Transcription saved at:\nTXT: {stt_txt_path}\nJSON: {stt_json_path}")

# Step 3: Analyze the transcription with the Gemini model
prompt = f"Analyze the following text for topic understanding and provide a comprehensive analysis:\n\n{transcription_text}"

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")
print("Making LLM inference request...")
response = model.generate_content([prompt], request_options={"timeout": 600})

# Save the analysis as TXT and JSON
analysis_txt_path = os.path.join(stt_dir, "Test-1-analysis.txt")
analysis_json_path = os.path.join(stt_dir, "Test-1-analysis.json")

with open(analysis_txt_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(response.text)

with open(analysis_json_path, 'w', encoding='utf-8') as json_file:
    json.dump({'analysis': response.text}, json_file, ensure_ascii=False, indent=4)

print(f"Analysis saved at:\nTXT: {analysis_txt_path}\nJSON: {analysis_json_path}")
print("Done!")
