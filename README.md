# Analysis-of-body-language-and-speech-in-video
Analysis of body language and speech in video with LLMs

**Analysis of Body Language and Speech in Video with LLMs**

This project analyzes body language and speech in video files using Large Language Models (LLMs). It extracts audio from videos, transcribes the speech, and then uses AI models for both text and body language analysis. The tool combines video processing, speech-to-text conversion, and advanced language analysis for comprehensive insights.

**Features**

Extracts audio from video.
Transcribes speech using the Whisper model.
Analyzes transcription for topic understanding with Gemini AI.
Performs body language analysis based on video content.
Video to Audio Conversion: Extracts audio from video files in MP4 format.
Speech-to-Text: Transcribes the extracted audio to text using the Whisper model.
Text Analysis: Analyzes the transcription for topic understanding and generates insightful content using Google Gemini AI.
Body Language Analysis: Analyzes the body language in the video by examining facial expressions, gestures, and movements.

-----
**how to run **:
1- install all library we need:

```bash
pip install -r requirements.txt
```

2- set the path of video in the main.py file :

```bash
# Paths for video, audio, and transcription output
video_file_path = "Your-path"
audio_dir = "Your-path"
stt_dir = "Your-path"
output_dir = "Your-path"

```

3-set the api key of your LLM(Gemeni) : 

```bash
# Configure the Gemini API key
GOOGLE_API_KEY = 'Your-key'  # Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)
```

4-just run main.py:

```bash
python main.py
```

**Example video :**


![1119](https://github.com/user-attachments/assets/02a9fcaa-a5ad-4fec-88a4-3f07d1c2443f)

Examples folder and file :
In the sample folder, all the examples are ready

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Communication with developers:

x(twitter) : https://x.com/Bugsbuuny2010

E-mail : dev.bugsbunny2000@gmail.com

Discord server to ask questions : https://discord.gg/6kVCyy6h

