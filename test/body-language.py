import google.generativeai as genai
from IPython.display import Markdown
import time
import json
import os

# Configure the API key
GOOGLE_API_KEY = 'Your-key'
genai.configure(api_key=GOOGLE_API_KEY)

# Define the video file path and output directory
video_file_name = "Your-path"
output_dir = "Your-path"

# Ensure the output directory exists

os.makedirs(output_dir, exist_ok=True)

# Upload the video file
print(f"Uploading file...")
video_file = genai.upload_file(path=video_file_name)
print(f"Completed upload: {video_file.uri}")

# Wait for the file to process
while video_file.state.name == "PROCESSING":
    print('.', end='')
    time.sleep(10)
    video_file = genai.get_file(video_file.name)

if video_file.state.name == "FAILED":
    raise ValueError("Video processing failed.")

# Create a comprehensive body language analysis prompt
prompt = """
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
And at the last then give a complete analysis of these factors and tell the strengths and weaknesses and suggestions for improvement
"""

# Choose the Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# Make the LLM inference request
print("Making LLM inference request...")
response = model.generate_content([video_file, prompt], request_options={"timeout": 600})

# Save the response as a JSON file
output_base_name = os.path.splitext(os.path.basename(video_file_name))[0]
json_output_path = os.path.join(output_dir, f"{output_base_name}.json")
txt_output_path = os.path.join(output_dir, f"{output_base_name}.txt")

# Write JSON output
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json.dump({'analysis': response.text}, json_file, ensure_ascii=False, indent=4)

# Write TXT output
with open(txt_output_path, 'w', encoding='utf-8') as txt_file:
    txt_file.write(response.text)

print(f"Analysis saved as:\nJSON: {json_output_path}\nTXT: {txt_output_path}")

# Display the response as Markdown for readability
Markdown(response.text)
