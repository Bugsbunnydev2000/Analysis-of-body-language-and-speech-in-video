import google.generativeai as genai
from IPython.display import Markdown
import time

GOOGLE_API_KEY = ('Your-key')

genai.configure(api_key=GOOGLE_API_KEY)
video_file_name = "Your path "

print(f"Uploading file...")
video_file = genai.upload_file(path=video_file_name)
print(f"Completed upload: {video_file.uri}")

# Check whether the file is ready to be used.
while video_file.state.name == "PROCESSING":
    print('.', end='')
    time.sleep(10)
    video_file = genai.get_file(video_file.name)

if video_file.state.name == "FAILED":
  raise ValueError(video_file.state.name)
# Create the prompt.
prompt = "I want you to analyze the user's body language from this video, such as hand, head, and foot movements, facial emotions, eye contact, gestures, and body postures."

# Choose a Gemini model.
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# Make the LLM request.
print("Making LLM inference request...")
response = model.generate_content([video_file, prompt],
                                  request_options={"timeout": 600})

# Print the response, rendering any Markdown
Markdown(response.text)