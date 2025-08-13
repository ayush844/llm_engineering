# Starting the process:

```bash

Last login: Fri Aug  8 21:28:17 on ttys000
(base) ayushsharma@lucas2o ~ % cd Desktop 
(base) ayushsharma@lucas2o Desktop % cd llm-projects 
(base) ayushsharma@lucas2o llm-projects % cd llm_engineering 
(base) ayushsharma@lucas2o llm_engineering % conda activate llms
(llms) ayushsharma@lucas2o llm_engineering % jupyter lab 

```

---

# **Beautiful Soup** 

## 1️⃣ What is Beautiful Soup?

**Beautiful Soup** is a **Python library for parsing HTML and XML** documents.
It’s mainly used for **web scraping** — extracting data from websites.

It:

* Turns messy HTML into a navigable parse tree.
* Lets you search for tags, attributes, and text easily.
* Works with parsers like:

  * Python’s built-in `html.parser` (slower, built-in)
  * `lxml` (faster, requires installation)
  * `html5lib` (handles broken HTML best)

---

## 2️⃣ Installing Beautiful Soup

```bash
pip install beautifulsoup4
pip install lxml        # optional, but faster parsing
```

---

## 3️⃣ Basic Usage

### Example HTML:

```html
<html>
  <head><title>Example Page</title></head>
  <body>
    <h1>Hello World</h1>
    <p class="intro">Welcome to the example page.</p>
    <a href="https://example.com/page1">Link 1</a>
    <a href="https://example.com/page2">Link 2</a>
  </body>
</html>
```

### Parsing it:

```python
from bs4 import BeautifulSoup

html_doc = """..."""  # put the HTML here
soup = BeautifulSoup(html_doc, 'lxml')  # or 'html.parser'
```

---

## 4️⃣ Finding Elements

Beautiful Soup gives you **methods to search** the HTML tree.

### 4.1 `find()` – First match

```python
title_tag = soup.find('title')
print(title_tag.text)  # Example Page
```

### 4.2 `find_all()` – All matches

```python
links = soup.find_all('a')
for link in links:
    print(link['href'])
```

### 4.3 Searching by **class**, **id**, or attributes

```python
intro = soup.find('p', class_='intro').text
print(intro)  # Welcome to the example page.

link2 = soup.find('a', href="https://example.com/page2").text
print(link2)
```

---

## 5️⃣ Navigating the Tree

```python
h1_tag = soup.h1
print(h1_tag.text)       # Hello World
print(h1_tag.name)       # h1
print(h1_tag.parent)     # <body> ... </body>
```

---

## 6️⃣ CSS Selectors (`select`)

```python
for link in soup.select('a'):
    print(link.get('href'))
```

CSS selector examples:

* `soup.select("p.intro")` → `<p>` tags with class `intro`
* `soup.select("a[href]")` → `<a>` tags with `href` attribute
* `soup.select("div > p")` → `<p>` tags directly inside a `<div>`

---

## 7️⃣ Extracting Text and Attributes

```python
link = soup.find('a')
print(link.get('href'))  # link URL
print(link.text)         # visible text
```

---

## 8️⃣ Real Example with Requests

```python
import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

quotes = soup.find_all('span', class_='text')
for q in quotes:
    print(q.text)
```

---

## 9️⃣ Common Use Cases

* Scraping blog posts
* Extracting product prices
* Getting headlines from news sites
* Collecting links, images, or tables

---

## 🔟 Important Notes

* **Respect websites’ terms of service** — some forbid scraping.
* Add delays between requests to avoid being blocked.
* Always use **`robots.txt`** to check if scraping is allowed.
* For dynamic websites (JavaScript-heavy), Beautiful Soup **alone** won’t work — you may need **Selenium** or **Playwright**.

---

💡 **Quick Mental Model:**
Beautiful Soup is like a *"searchable map"* of a webpage.
You give it HTML, it gives you **Python objects** you can search, navigate, and extract data from.

---
---
---


# **System prompts** and **User prompts**

---

## 1️⃣ **User Prompt**

* **What it is:**
  The text or instructions *you* (the human) give to the AI.
  It tells the AI **what you want** and **how you want it**.

* **Purpose:**
  Guides the AI’s immediate output for a specific request.

* **Example:**

  > "Write me a short poem about the ocean in the style of Shakespeare."
  > Here, you are the *user* giving the *user prompt*.

---

## 2️⃣ **System Prompt**

* **What it is:**
  A hidden or predefined instruction given to the AI **before** your prompt.
  It sets the **rules, personality, tone, and behavior** for the entire conversation.

* **Purpose:**
  Defines how the AI should behave **regardless** of what the user asks.
  It’s like the “character sheet” or “operating manual” for the AI.

* **Example:**
  The system prompt might be something like:

  > "You are ChatGPT, a large language model trained by OpenAI. Always answer helpfully, truthfully, and concisely."
  > You don’t usually see this in normal chat — it’s running in the background.

---

## 3️⃣ **How They Work Together**

* **System Prompt:** The *big picture* rules ("Be polite, be safe, don’t break the law").
* **User Prompt:** The *specific request* ("Explain quantum mechanics like I’m 5").
* The AI’s response = **System Prompt + User Prompt + Model Training**.

---

## 4️⃣ Analogy

Think of it like a **role-play game**:

* **System Prompt** = The game master saying *"You’re a wise old wizard who always speaks in riddles."*
* **User Prompt** = The player saying *"Tell me how to find the magic sword."*
* **Response** = Wizard answer, but still in riddle form, because the system prompt says so.

---

