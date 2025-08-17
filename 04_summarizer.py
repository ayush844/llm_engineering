"""
summarizer.py

A simple script that:
1. Loads your OpenAI API key from a .env file
2. Fetches a website’s HTML content
3. Cleans up unnecessary tags (script, style, etc.)
4. Extracts the readable text
5. Sends the text to OpenAI to generate a markdown summary
6. Prints the summary in the terminal

Requirements:
- requests
- beautifulsoup4
- python-dotenv
- openai

Install dependencies:
    pip install requests beautifulsoup4 python-dotenv openai
"""

import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI

# ------------------------------------------------------------
# 1. Load the API key
# ------------------------------------------------------------

# Loads variables from .env into environment variables
load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "❌ No API key found. Please create a .env file with OPENAI_API_KEY=your_key_here"
    )
elif not api_key.startswith("sk-proj-"):
    print("⚠️ API key found, but it doesn't look like a project key (sk-proj-...)")
elif api_key.strip() != api_key:
    print("⚠️ API key has spaces or tabs around it. Please remove them.")
else:
    print("✅ API key found and looks valid.")

# Initialize OpenAI client
openai = OpenAI(api_key=api_key)

# ------------------------------------------------------------
# 2. Website class for scraping + cleaning text
# ------------------------------------------------------------

class Website:
    """
    Represents a website and extracts its text content using BeautifulSoup.
    """

    def __init__(self, url: str):
        """
        Initialize the Website object with title and cleaned text content.
        Removes irrelevant tags such as <script>, <style>, <img>, <input>.
        """
        self.url = url

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/117.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch {url}. Status code: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract title
        self.title = soup.title.string.strip() if soup.title else "No title found"

        # Remove irrelevant elements
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            # Extract readable text
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""

# ------------------------------------------------------------
# 3. OpenAI prompt preparation
# ------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are an assistant that analyzes the contents of a website "
    "and provides a short summary, ignoring text that might be navigation related. "
    "Respond in markdown."
)

def user_prompt_for(website: Website) -> str:
    """
    Create the user prompt that feeds the website text into the LLM.
    """
    return (
        f"You are looking at a website titled {website.title}\n\n"
        "The contents of this website are as follows; "
        "please provide a short summary of this website in markdown. "
        "If it includes news or announcements, then summarize these too.\n\n"
        f"{website.text}"
    )

def messages_for(website: Website):
    """
    Returns the conversation messages to send to OpenAI.
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt_for(website)},
    ]

# ------------------------------------------------------------
# 4. Summarization functions
# ------------------------------------------------------------

def summarize(url: str) -> str:
    """
    Fetch a website, send its text to OpenAI, and return the summary.
    """
    website = Website(url)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for(website),
    )
    return response.choices[0].message.content

def display_summary(url: str):
    """
    Print a markdown-style summary of the given website.
    """
    summary = summarize(url)
    print("\n" + "="*60)
    print(f"Summary of {url}:")
    print("="*60)
    print(summary)
    print("="*60 + "\n")

# ------------------------------------------------------------
# 5. Run if script is executed directly
# ------------------------------------------------------------

if __name__ == "__main__":
    test_url = "https://edwarddonner.com"
    display_summary(test_url)




# (venv) (base) ayushsharma@lucas2o llm_engineering % python 04_summarizer.py

# /Users/ayushsharma/Desktop/ayush_llm/llm_engineering/venv/lib/python3.9/site-packages/urllib3/__init__.py:35: NotOpenSSLWarning: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'LibreSSL 2.8.3'. See: https://github.com/urllib3/urllib3/issues/3020
#   warnings.warn(
# ✅ API key found and looks valid.

# ============================================================
# Summary of https://edwarddonner.com:
# ============================================================
# # Summary of Edward Donner's Website

# Edward Donner's website serves as a personal platform where he showcases his interests in coding, experimentation with large language models (LLMs), and his background in electronic music and technology. 

# ## About Ed
# - **Profession**: Co-founder and CTO of **Nebula.io**, which focuses on AI solutions for talent discovery and management.
# - **Experience**: Former founder and CEO of **untapt**, an AI startup acquired in 2021.
# - **Expertise**: Knowledgeable in developing proprietary LLMs specific to the talent industry, with a patented matching model and successful product deployment.

# ## Recent Posts and Announcements
# 1. **Connecting my courses – become an LLM expert and leader** - May 28, 2025
# 2. **2025 AI Executive Briefing** - May 18, 2025
# 3. **The Complete Agentic AI Engineering Course** - April 21, 2025
# 4. **LLM Workshop – Hands-on with Agents – resources** - January 23, 2025

# The website encourages connection with Ed and offers insights into his professional endeavors and educational initiatives in the AI and LLM space.
# ============================================================
