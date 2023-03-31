import bs4
import requests
import typing
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nametolink import name_to_link
# Hot or Not

DEBUG = 0  # Set this to 1 to get more console output

# Lexicons for opinion lexicon sentiment analysis
positive_lexicon = []
negative_lexicon = []


class ProfessorRating:
    # Possible attributes, edit as needed
    true_rating = 0  # from website scale
    homemade_rating = None
    sentiment_method = None
    label = ""  # e.g. "Hot", "not hot" or "mid"
    name = ""  # self-explanatory
    # direct link to this specific professor's page
    website_link = "ratemyprofessors.com"
    # which university this professor teaches for
    university = "University of Michigan"
    comments = []  # Comments scraped from ratemyprofessors

    def __init__(self, name, rating, link, university, comments):
        self.name = name
        self.true_rating = rating
        self.website_link = link
        self.university = university
        self.comments = comments

    def true_rating(self):
        return self.true_rating

    def rating(self):
        return self.rating

    def how_hot(self):
        return self.label

    def print_summary(self):
        x = "Professor "+self.name+" is a professor at the "+self.university + \
            " who has had comments written by " + \
            str(len(self.comments))+" students.\n"
        if self.sentiment_method != None:
            x += "Using the "+self.sentiment_method+" method, professor " + \
                self.name+" has a rating of "+str(self.homemade_rating)+".\n"
            x += "The true rating from ratemyprofessors is " +\
                str(self.true_rating)+".\n"
        return x


def clean(comment: str) -> str:
    # Clean up a comment so that its ready for text processing TODO
    return comment.translate(str.maketrans('', '', string.punctuation))


def scrape(link: str, name: str, university: str) -> ProfessorRating:
    # Scrape the website, but this time with selenium so we can click the button

    # Initialize headless chromium webdriver
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Chrome(options=options)

    if DEBUG:
        print("Successfully intialized Chrome headless webbrowser.")

    # Get the ratemyprofessor page
    driver.get(link)
    if DEBUG:
        print(f"Page title: {driver.title}")

    # close cookies reminder
    button = driver.find_element(By.CLASS_NAME, "gvGrz")
    if DEBUG:
        print(f"Attempting to click button with text: {button.text}")
    button.click()

    # Get true rating, name, and university
    true_rating = float(driver.find_element(By.CLASS_NAME, "liyUjw").text)
    if DEBUG:
        print(f"True rating scraped: {true_rating}")

    # name = driver.find_element(By.CLASS_NAME, "cfjPUG").text
    # if DEBUG:
    #     print(f"Name scraped: {name}")
    # university_string = driver.find_element(By.CLASS_NAME, 'iLYGwn').text
    # if DEBUG:
    #     print(f"University string scraped: {university_string}")
    # univeristy = university_string[university_string.find('at')+3:]

    # Note: this is probably a really lazy way to do the university name, but I was having
    # a lot of trouble with using xpath to find the actual <a> tag I needed for just the university name
    # so I settled with getting the entire string (university_string) and just truncated it as needed

    # Try and actually use selenium for what we need it for, clicking buttons for more comments
    try:
        while (True):
            # Wait until either the "load more results" button exists, or 5 seconds have passed
            moreCommentButton = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'gjQZal'))
            )
            if DEBUG:
                print(
                    f"Attempting to click button with text: {moreCommentButton.text}")
            # Click the button if it exists, if its not clickable, we're done so exit the loop
            moreCommentButton.click()
    except:
        if DEBUG:
            print(f"hopefully got all the comments by now")

    # In theory, all comments on page now, all with the class 'gRjWel', attempting to scrape them
    comments = []
    comments_div = driver.find_elements(By.CLASS_NAME, 'gRjWel')
    for driver_element in comments_div:
        comments.append(clean(driver_element.text))
    driver.close()

    if DEBUG:
        print(f"Webdriver successfully closed. Attempting to initialize professor and return from scrape function.")
    professor = ProfessorRating(name, true_rating, link, university, comments)
    return professor


def scrape_deprecated(link: str) -> ProfessorRating:
    # Scrape the ratemyprofessors website with the given link to find information about a professor

    # Get the page
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(link, headers=headers)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

    # Find true rating
    true_rating = float(
        soup.find("div", {"class": "RatingValue__Numerator-qw8sqy-2 liyUjw"}).next)*2

    # Find name and university
    name_div = soup.find("div", {"class": "NameTitle__Name-dowf0z-0 cfjPUG"})
    first_name = name_div.next.next
    last_name = name_div.find(
        "span", {"class": "NameTitle__LastNameWrapper-dowf0z-2 glXOHH"}).next
    university = name_div.next_sibling.contents[1].next

    # Load all the comments

    # Find comments
    comments = []
    comments_div = soup.find_all(
        "div", {"class": "Comments__StyledComments-dzzyvm-0 gRjWel"})
    for comment in comments_div:
        comments.append(clean(comment.next))

    professor = ProfessorRating(
        (first_name+" "+last_name), true_rating, link, university, comments)
    return professor


def opinion_lexicon(comment_list: typing.List[str]) -> float:
    # This method takes in the comments from a professor and uses the opinion lexicons to generate a rating.
    global positive_lexicon
    global negative_lexicon
    score = 0
    wc = 0
    for comment in comment_list:
        for word in comment.split(" "):
            stopword = True
            if word in positive_lexicon:
                score = score + 1
                stopword = False
            if word in negative_lexicon:
                score = score - 1
                stopword = False
            if not stopword:
                wc += 1
    # Formula derived as follows. 
    # First, look through all words in all comments.
    # If a given word is in positive_lexicon, add one to the score
    # If a given word is in negative_lexicon, subtract one from the score
    # If a given word is in either, add one to the "non-stopword word count" (wc)
    # Normalize the score by the wordcount, such that 0 positive words would return a score of 0
    # and all positive words returns a score of 10
    return round(((score)/wc) * 5 + 5, 1)


def call(x, y, z):
    global positive_lexicon
    global negative_lexicon
    with open("negative-words.txt") as f:
        for line in f:
            negative_lexicon.append(line.strip())
    with open("positive-words.txt") as f:
        for line in f:
            positive_lexicon.append(line.strip())

    # link = input(
    #     "Enter the link of a professor you want to learn about, or STOP to exit: ")
    # if link.lower() == "stop" or link.lower() == 'exit':
    #     break
    try:
        link, name, university = name_to_link(x, y)
    except:
        return 1

    try:
        professor = scrape(link, name, university)
        # professor = scrape("http://www.ratemyprofessors.com/professor?tid=140940")
    except Exception as e:
        print("Invalid link")
        print(e)
        return 1
    # print("Evaluation methods:")
    # print("1. Opinion Lexicons: This method solely uses the total" +
    #       "number of positive and negative words to try and determine " +
    #       "the overall sentiment of the comments to generate a rating score")
    # print("2. [Under Construction]")
    # choice = int(input("Which method would you like (enter the number): "))
    choice = int(z)
    if choice == 1:
        professor.homemade_rating = opinion_lexicon(professor.comments)
        professor.sentiment_method = "Opinion Lexicon"
    else:
        print("Choice not valid")
    return professor.print_summary()


if __name__ == "__main__":
    call()
