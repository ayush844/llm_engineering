"""
brochure_maker.py

This script:
1. Loads your OpenAI API key from a .env file
2. Fetches a company website (landing page + relevant pages like About/Careers)
3. Uses OpenAI to decide which links are relevant for a company brochure
4. Scrapes the text from those links
5. Asks OpenAI to create a short brochure in markdown format
6. Prints the result in the terminal

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
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI

# ------------------------------------------------------------
# 1. Load API key
# ------------------------------------------------------------
load_dotenv(override=True)  # loads variables from .env into environment variables
api_key = os.getenv("OPENAI_API_KEY")

if api_key and api_key.startswith("sk-proj-") and len(api_key) > 10:
    print("✅ API key looks good so far")
else:
    raise ValueError(
        "❌ There might be a problem with your API key. "
        "Please check your .env file and make sure it has: OPENAI_API_KEY=sk-proj-xxxx..."
    )

# Initialize OpenAI client
openai = OpenAI(api_key=api_key)
MODEL = "gpt-4o-mini"

# A User-Agent header is needed to avoid websites blocking our scraper
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/117.0.0.0 Safari/537.36"
    )
}

# ------------------------------------------------------------
# 2. Website class for scraping
# ------------------------------------------------------------
class Website:
    """
    A utility class that represents a website page:
    - Stores the page's title
    - Extracts readable text (removes scripts, images, etc.)
    - Collects all links on the page
    """

    def __init__(self, url: str):
        self.url = url
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            raise Exception(f"❌ Failed to fetch {url}. Status code: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")

        # Page title
        self.title = soup.title.string if soup.title else "No title found"

        # Extract readable text (ignoring scripts, styles, etc.)
        if soup.body:
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = ""

        # Extract all hyperlinks from the page
        links = [link.get("href") for link in soup.find_all("a")]
        # Filter out None values (broken links)
        self.links = [link for link in links if link]

    def get_contents(self) -> str:
        """
        Returns a string containing the title and text of this page.
        """
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

# ------------------------------------------------------------
# 3. Prompt for selecting relevant links
# ------------------------------------------------------------
link_system_prompt = (
    "You are provided with a list of links found on a webpage. "
    "You are able to decide which of the links would be most relevant to include "
    "in a brochure about the company, such as links to an About page, Company page, or Careers/Jobs pages.\n"
    "You should respond in JSON as in this example:\n"
    "{\n"
    '    "links": [\n'
    '        {"type": "about page", "url": "https://full.url/goes/here/about"},\n'
    '        {"type": "careers page", "url": "https://another.full.url/careers"}\n'
    "    ]\n"
    "}\n"
)

def get_links_user_prompt(website: Website) -> str:
    """
    Build the user prompt for the model:
    - Show the list of links
    - Ask it to select which ones are relevant to a company brochure
    """
    user_prompt = (
        f"Here is the list of links on the website of {website.url}. "
        "Please decide which of these are relevant web links for a brochure about the company. "
        "Respond with the full https URL in JSON format. "
        "Do not include Terms of Service, Privacy, or email links.\n\n"
        "Links (some might be relative links):\n"
    )
    user_prompt += "\n".join(website.links)
    return user_prompt

def get_links(url: str) -> dict:
    """
    Fetch the website and ask GPT to pick relevant links.
    Returns a dictionary with selected links.
    """
    website = Website(url)
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": link_system_prompt},
            {"role": "user", "content": get_links_user_prompt(website)},
        ],
        response_format={"type": "json_object"},  # Ensures JSON output
    )
    result = response.choices[0].message.content
    return json.loads(result)  # Convert JSON string -> Python dictionary

# ------------------------------------------------------------
# 4. Gather all page details (landing + relevant links)
# ------------------------------------------------------------
def get_all_details(url: str) -> str:
    """
    Collects the contents of the landing page and any relevant sub-pages (About, Careers, etc.)
    """
    result = "Landing page:\n"
    result += Website(url).get_contents()

    links = get_links(url)
    print("🔗 Found relevant links:", links)

    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += Website(link["url"]).get_contents()

    return result

# ------------------------------------------------------------
# 5. Prompt for brochure creation
# ------------------------------------------------------------
system_prompt = (
    "You are an assistant that analyzes the contents of several relevant pages "
    "from a company website and creates a short brochure about the company "
    "for prospective customers, investors, and recruits. Respond in markdown. "
    "Include details of company culture, customers, and careers/jobs if available."
)

def get_brochure_user_prompt(company_name: str, url: str) -> str:
    """
    Build the prompt with company name + contents of pages.
    We truncate to 5000 characters so it doesn't exceed model limits.
    """
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += (
        "Here are the contents of its landing page and other relevant pages; "
        "use this information to build a short brochure of the company in markdown.\n"
    )
    user_prompt += get_all_details(url)
    return user_prompt[:5_000]  # keep only first 5000 characters

# ------------------------------------------------------------
# 6. Create brochure
# ------------------------------------------------------------
def create_brochure(company_name: str, url: str) -> str:
    """
    Main function that creates a brochure by:
    1. Collecting relevant content from website
    2. Asking OpenAI to generate a markdown brochure
    Returns the brochure as a string
    """
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": get_brochure_user_prompt(company_name, url)},
        ],
    )
    result = response.choices[0].message.content
    return result


# With a small adjustment, we can change this so that the results stream back from OpenAI, with the familiar typewriter animation:

# def stream_brochure(company_name, url):
#     stream = openai.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
#           ],
#         stream=True
#     )
    
#     response = ""
#     display_handle = display(Markdown(""), display_id=True)
#     for chunk in stream:
#         response += chunk.choices[0].delta.content or ''
#         response = response.replace("```","").replace("markdown", "")
#         update_display(Markdown(response), display_id=display_handle.display_id)

# ------------------------------------------------------------
# 7. Run script directly
# ------------------------------------------------------------
if __name__ == "__main__":
    company_name = "HuggingFace"
    url = "https://huggingface.co"

    print(f"📄 Generating brochure for {company_name} ({url}) ...\n")

    brochure = create_brochure(company_name, url)

    print("=" * 60)
    print(f"Brochure for {company_name}")
    print("=" * 60)
    print(brochure)
    print("=" * 60)
