import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

# add a requirement in requirements.txt

# requirements.txt
# selenium
# beautifulsoup4
# requests
# openai
# ipython
# python-dotenv

# pip install -r requirements.txt


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Check the key
def check_key(api_key):
    """
    first add api key in .env file. EX- OPENAI_API_KEY=your_api_key
    """
    if not api_key:
        print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
    elif not api_key.startswith("sk-proj-"):
        print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
    elif api_key.strip() != api_key:
        print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
    else:
        print("API key found and looks good so far!")

# check_key(api_key)

openai = OpenAI()


class Website:

    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)







site = Website("https://www.cnn.com")

# print(site.title)
# print(site.text)

# Define our system prompt - you can experiment with this later, changing the last sentence to 'Respond in markdown in Spanish."
system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."


# A function that writes a User Prompt that asks for summaries of websites:
def user_prompt_for(website):
    """
    Return a user prompt for the given website that asks for a short summary in markdown.
    The prompt will include the title of the website, and the text of the website.
    """
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

# print(user_prompt_for(site))


def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

# print(messages_for(site)) 

def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages_for(website)
    )
    return response.choices[0].message.content

def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))

# runt this in jupyter lab
# display_summary("https://www.cnn.com") 


def save_summary_to_file(url, filename):
    summary = summarize(url)
    with open(filename, 'w') as f:
        f.write(summary) 


# add extension like md or txt.
save_summary_to_file("https://www.cnn.com", "cnn_summary.md") 








# for javascript rendering websites give code

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options

PATH_TO_CHROME_DRIVER = '..\\path\\to\\chromedriver.exe'

class Website:
    url: str
    title: str
    text: str

    def __init__(self, url):
        self.url = url

        options = Options()

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        service = Service(PATH_TO_CHROME_DRIVER)
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)

        input("Please complete the verification in the browser and press Enter to continue...")
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.get_text(separator="\n", strip=True)


