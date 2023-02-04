import os
import openai
from key import key
from train import train

os.environ["PYTHONIOENCODING"] = "utf-8"
openai.api_key = key
model = "text-davinci-003"
temperature=0
max_tokens=300