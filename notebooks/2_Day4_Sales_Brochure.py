import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import display, Markdown
from scraper import summarize_dynamic_site, get_links

load_dotenv(override = True)
api_key = os.getenv("MY_OPENAI_API_KEY")
openai = OpenAI(api_key = api_key)
MODEL = "gpt-4o-mini"

links = get_links("https://en.wikipedia.org/wiki/Main_Page") # Use Wikipedia
print(links)
