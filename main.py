#Impoet all library we need
import os
import time
import json
from moviepy.editor import VideoFileClip
import whisper
import google.generativeai as genai
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich import print as rprint
from colorama import init, Fore, Style
from IPython.display import Markdown

# Initialize colorama for cross-platform color support
init(autoreset=True)
colors = ["red", "green", "yellow", "blue", "magenta", "cyan", "white"]
# Configure the Gemini API key
GOOGLE_API_KEY = 'Your-key'  # Replace with your actual key
genai.configure(api_key=GOOGLE_API_KEY)

# Paths for video, audio, and transcription output
video_file_path = "Your-path"
audio_dir = "Your-path"
stt_dir = "Your-path"
output_dir = "Your-path"

# Ensure necessary directories exist
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(stt_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Create a rich console instance for better terminal output
console = Console()

# Fun introductory message with rich colors and emojis
rprint("[bold magenta]|￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣|[/bold magenta]")
rprint("[bold magenta]| [green]Bugs-bunny Terminal: Let's hop into action![/green] |[/bold magenta]")
rprint("[bold magenta]|＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿＿|[/bold magenta]")
rprint("[yellow]     (•◡•)[/yellow]    [cyan]✨ Time for some magic![/cyan]")
rprint("[cyan]     \\   /[/cyan]")
rprint("[cyan]      ——[/cyan]")
rprint("[cyan]      |   |[/cyan]")
rprint("[cyan]      |_  _|[/cyan]")

# Step 1: Convert video to audio (MP3)
console.print("\n[bold blue]Step 1:[/bold blue] [yellow]Converting video to audio...[/yellow]")
with Progress(
    SpinnerColumn(style="cyan"), BarColumn(bar_width=30, complete_style="green"), TextColumn("[progress.description]{task.description}"), console=console
) as progress:
    task = progress.add_task("[cyan]Extracting audio from video...", total=1)
    time.sleep(1)  # Simulate processing time for user experience
    audio_file_path = os.path.join(audio_dir, "Test-1.mp3")
    video_clip = VideoFileClip(video_file_path)
    video_clip.audio.write_audiofile(audio_file_path)
    video_clip.close()
    progress.update(task, completed=1)
    progress.stop()

rprint("[bold green]✓[/bold green] [green]Audio extraction complete![/green]")

# Step 2: Transcribe audio using the local Whisper model
console.print("\n[bold blue]Step 2:[/bold blue] [yellow]Transcribing audio with Whisper...[/yellow]")
with Progress(
    SpinnerColumn(style="magenta"), BarColumn(bar_width=30, complete_style="yellow"), TextColumn("[progress.description]{task.description}"), console=console
) as progress:
    task = progress.add_task("[magenta]Transcribing audio...", total=1)
    time.sleep(1.5)  # Simulate processing time for user experience
    whisper_model = whisper.load_model("base")  # Load Whisper model
    transcription_result = whisper_model.transcribe(audio_file_path)
    progress.update(task, completed=1)
    progress.stop()

# Save transcription as TXT and JSON
transcription_text = transcription_result['text']
stt_txt_path = os.path.join(stt_dir, "Test-1.txt")
stt_json_path = os.path.join(stt_dir, "Test-1.json")

with open(stt_txt_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(transcription_text)

with open(stt_json_path, 'w', encoding='utf-8') as json_file:
    json.dump({'transcription': transcription_text}, json_file, ensure_ascii=False, indent=4)

rprint("[bold green]✓[/bold green] [green]Transcription complete![/green]")
console.print(f"[bold green]Files saved:[/bold green]\n[green]TXT:[/green] {stt_txt_path}\n[green]JSON:[/green] {stt_json_path}")

# Step 3: Analyze the transcription with the Gemini model
console.print("\n[bold blue]Step 3:[/bold blue] [yellow]Analyzing transcription with Gemini model...[/yellow]")
prompt = f"Analyze the following text for topic understanding and provide a comprehensive analysis:\n\n{transcription_text}"
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

with Progress(
    SpinnerColumn(style="green"), BarColumn(bar_width=30, complete_style="cyan"), TextColumn("[progress.description]{task.description}"), console=console
) as progress:
    task = progress.add_task("[green]Generating content...", total=1)
    time.sleep(2)  # Simulate processing time for user experience
    response = model.generate_content([prompt], request_options={"timeout": 600})
    progress.update(task, completed=1)
    progress.stop()

# Save the analysis as TXT and JSON
analysis_txt_path = os.path.join(stt_dir, "Test-1-analysis.txt")
analysis_json_path = os.path.join(stt_dir, "Test-1-analysis.json")

with open(analysis_txt_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(response.text)

with open(analysis_json_path, 'w', encoding='utf-8') as json_file:
    json.dump({'analysis': response.text}, json_file, ensure_ascii=False, indent=4)

# Step 4: Perform body language analysis
console.print("\n[bold blue]Step 4:[/bold blue] [yellow]Performing body language analysis...[/yellow]")
prompt_body_language = """
Analyze the body language in the provided video, focusing on the following aspects:
1. Facial expressions and emotional cues (e.g., smiles, frowns, raised eyebrows).
2. Eye gaze direction and eye contact patterns.
3. Head movements and tilts.
4. Body posture (e.g., leaning forward or backward, open or closed stance).
5. Hand and arm movements (e.g., gestures, folding arms, pointing).
6. The position and movement of the legs (e.g., crossed legs, shifting weight).
7. Subtle movements such as touching the face, playing with fingers, or adjusting clothing.
8. Sweating or visible skin reactions.
9. The rhythm and pacing of movements.
10. Micro-expressions and subtle shifts in demeanor.
And at the last, provide a complete analysis, highlighting strengths, weaknesses, and suggestions for improvement.
"""

# Upload the video file for analysis
print(f"Uploading file for body language analysis...")
video_file = genai.upload_file(path=video_file_path)
print(f"Completed upload: {video_file.uri}")

# Wait for the file to process
while video_file.state.name == "PROCESSING":
    print('.', end='')
    time.sleep(10)
    video_file = genai.get_file(video_file.name)

if video_file.state.name == "FAILED":
    raise ValueError("Video processing failed.")

# Make the LLM inference request for body language analysis
print("Making LLM inference request for body language...")
response_body = model.generate_content([video_file, prompt_body_language], request_options={"timeout": 600})

# Save the body language analysis as TXT and JSON
body_analysis_txt_path = os.path.join(output_dir, "Test-1-body-analysis.txt")
body_analysis_json_path = os.path.join(output_dir, "Test-1-body-analysis.json")

with open(body_analysis_txt_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(response_body.text)

with open(body_analysis_json_path, 'w', encoding='utf-8') as json_file:
    json.dump({'body_analysis': response_body.text}, json_file, ensure_ascii=False, indent=4)

rprint("[bold green]✓ Body language analysis complete![/bold green]")
console.print(f"[bold green]Files saved:[/bold green]\n[green]TXT:[/green] {body_analysis_txt_path}\n[green]JSON:[/green] {body_analysis_json_path}")

# Display the body language analysis in Markdown format
Markdown(response_body.text)

# Final fun message with emojis
rprint("[bold magenta]🎉 All tasks complete! Have an amazing day! 🎉[/bold magenta]")
rprint("[yellow]Remember: Great code comes with great coffee! ☕[/yellow]")
