import typing
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nametolink import name_to_link
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from naivebayes import trainNaiveBayes, testNaiveBayes
# Hot or Not

DEBUG = 0  # Set this to 1 to get more console output

# Lexicons for opinion lexicon sentiment analysis
positive_lexicon = []
negative_lexicon = []
professor_table = {}
name_table = {}
bayesValues = []


def get_label(score):
    # TODO Someone make these better later, this is what I came up with on short notice
    if score < 1:
        return "🤮🤮🤮"
    if score < 2:
        return "🥶"
    if score < 3:
        return "🤧"
    if score < 4:
        return "⛈"
    if score < 5:
        return "Mid"
    if score < 6:
        return "🌤"
    if score < 7:
        return "☀️"
    if score < 8:
        return "☕️"
    if score < 9:
        return "🥵"
    if score < 9.5:
        return "🔥"
    if score < 10:
        return "🔥🧯🚒"


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

    def print_summary(self):
        print("Professor "+self.name+" has comments written by " +
              str(len(self.comments))+" students.")
        if self.sentiment_method != None:
            print(""+self.sentiment_method+" rating: " +
                  str(self.homemade_rating)+".")
            print("True rating from ratemyprofessors: " +
                  str(self.true_rating)+".")

    def return_summary(self):
        self.label = get_label(self.homemade_rating)
        return f"Professor {self.name} has had comments written by {len(self.comments)} students.\n {self.sentiment_method} rating: {self.homemade_rating} {self.label}\n Ratemyprofessor gives this professor a score of {self.true_rating}."


def clean(comment: str) -> str:
    # Clean up a comment so that its ready for text processing TODO
    return comment.translate(str.maketrans('', '', string.punctuation))


def scrape(link: str, name: str, university: str) -> ProfessorRating:
    # Scrape the website, but this time with selenium so we can click the button

    # Initialize headless chromium webdriver
    options = Options()
    options.add_argument('-headless')
    # options.add_argument("--incognito")
    # options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    # driver = webdriver.Chrome()

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
    true_rating = float(driver.find_element(By.CLASS_NAME, "liyUjw").text) * 2
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
    except Exception as e:
        if DEBUG:
            print(f"hopefully got all the comments by now")

    # In theory, all comments on page now, all with the class 'gRjWel', attempting to scrape them
    comments = []
    comments_div = driver.find_elements(By.CLASS_NAME, 'gRjWel')
    for driver_element in comments_div:
        comments.append(driver_element.text)
    driver.close()

    if DEBUG:
        print(f"Webdriver successfully closed. Attempting to initialize professor and return from scrape function.")
    professor = ProfessorRating(name, true_rating, link, university, comments)
    return professor


# def scrape_deprecated(link: str) -> ProfessorRating:
#     # Scrape the ratemyprofessors website with the given link to find information about a professor

#     # Get the page
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
#     page = requests.get(link, headers=headers)
#     soup = bs4.BeautifulSoup(page.text, 'html.parser')

#     # Find true rating
#     true_rating = float(
#         soup.find("div", {"class": "RatingValue__Numerator-qw8sqy-2 liyUjw"}).next)*2

#     # Find name and university
#     name_div = soup.find("div", {"class": "NameTitle__Name-dowf0z-0 cfjPUG"})
#     first_name = name_div.next.next
#     last_name = name_div.find(
#         "span", {"class": "NameTitle__LastNameWrapper-dowf0z-2 glXOHH"}).next
#     university = name_div.next_sibling.contents[1].next

#     # Load all the comments

#     # Find comments
#     comments = []
#     comments_div = soup.find_all(
#         "div", {"class": "Comments__StyledComments-dzzyvm-0 gRjWel"})
#     for comment in comments_div:
#         comments.append(comment.next)

#     professor = ProfessorRating(
#         (first_name+" "+last_name), true_rating, link, university, comments)
#     return professor


def opinion_lexicon(comment_list: typing.List[str]) -> float:
    # This method takes in the comments from a professor and uses the opinion lexicons to generate a rating.
    global positive_lexicon
    global negative_lexicon
    score = 0
    wc = 0
    for comment in comment_list:
        comment = clean(comment)
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


def vaderSentenceAnalysis(comment_list: typing.List[str]) -> float:
    # This method uses Vader Sentiment Analysis to classify individual sentences, weighting each sentence equally
    # This does give comments with more sentences in them greater impact on the score as a whole, which could be changed if we wanted TODO?
    score = 0
    total_sentences = 0
    analyzer = SentimentIntensityAnalyzer()
    for comment in comment_list:
        for sentence in comment.split("."):
            if sentence.strip() == '':
                continue
            vs = analyzer.polarity_scores(sentence)
            total_sentences += 1
            score += float(vs['compound'])
    return round((score/total_sentences) * 5 + 5, 1)


def vaderCommentAnalysis(comment_list: typing.List[str]) -> float:
    # This method uses Vader Sentiment Analysis to classify whole comments
    score = 0
    total_sentences = 0
    analyzer = SentimentIntensityAnalyzer()
    for comment in comment_list:
        vs = analyzer.polarity_scores(comment)
        score += float(vs['compound'])
    return round((score/len(comment_list)) * 5 + 5, 1)

def naiveBayesAnalysis(comment_list: typing.List[str]) -> float:
    total_pos = 0
    for comment in comment_list:
        verdict, _, _ = testNaiveBayes(bayesValues, comment)
        if verdict == "pos":
            total_pos += 1
    return round((total_pos/len(comment_list)) * 10, 1)

def call(name: str, university: str, option: str):
    # This method is called by the website to actually determine a professor's rating.
    option = int(option)
    global name_table
    # keep local name records including user typos
    if (name+university) in name_table:
        link, name, university = name_table[name+university]
    else:
        try:
            link, newname, newuniversity = name_to_link(name, university)
        except ValueError as e:
            return "Invalid Professor Credentials!"

        name_table[name+university] = (link, newname, newuniversity)
        name = newname
        university = newuniversity
    return getData(link, name, university, option)


def getData(link, name, university, option):
    professor = getProfessor(link, name, university)
    if option == 1:
        # Opinion lexicon
        professor.homemade_rating = opinion_lexicon(professor.comments)
        professor.sentiment_method = "Opinion Lexicon"
        return professor.return_summary()
    elif option == 3:
        # VADER Comment Analysis, reading the entire comment at once
        professor.homemade_rating = vaderCommentAnalysis(professor.comments)
        professor.sentiment_method = "VADER Comment Analysis"
        return professor.return_summary()
    elif option == 4:
        # VADER Setence Analysis, individually analyzing each sentence
        professor.homemade_rating = vaderSentenceAnalysis(professor.comments)
        professor.sentiment_method = "VADER Sentence Analysis"
        return professor.return_summary()
    elif option == 5:
        # Naive Bayes Analysis, using 100 random positive and negative comments
        professor.homemade_rating = naiveBayesAnalysis(professor.comments)
        professor.sentiment_method = "Naive Bayes Analysis"
        return professor.return_summary()
    else:
        return "You selected an option that wasn't implemented, sorry."


def getProfessor(link, name, university):
    # keep local professor records
    if link in professor_table:
        professor = professor_table[link]
    else:
        # scrape
        try:
            professor = scrape(link, name, university)
            professor_table[link] = professor
        except Exception as e:
            raise Exception("Problem with scraping")
    return professor


def main():
    while True:
        # link = input(
        #     "Enter the link of a professor you want to learn about, or STOP to exit: ")
        # if link.lower() == "stop" or link.lower() == 'exit':
        #     break
        try:
            link, name, university = name_to_link()
            # link = "http://www.ratemyprofessors.com/professor?tid=140940"
            # name = "Brian Noble"
            # university = "University of Michigan"
        except:
            break

        try:
            professor = scrape(link, name, university)
            # professor = scrape("http://www.ratemyprofessors.com/professor?tid=140940", "Brian Noble", "University of Michigan")
        except Exception as e:
            print("Invalid link")
            print(e)
            break
        print("Evaluation methods:")
        print("1. Opinion Lexicons: This method solely uses the total " +
              "number of positive and negative words to try and determine " +
              "the overall sentiment of the comments to generate a rating score")
        print("2. [Under Construction]")
        choice = int(input("Which method would you like (enter the number): "))
        if choice == 1:
            professor.homemade_rating = opinion_lexicon(professor.comments)
            professor.sentiment_method = "Opinion Lexicon"
        else:
            print("Choice not valid")
        professor.print_summary()


if __name__ == "__main__":
    main()

# Prime bayes and opinion lexicon

with open("negative-words.txt") as f:
    for line in f:
        negative_lexicon.append(line.strip())
with open("positive-words.txt") as f:
    for line in f:
        positive_lexicon.append(line.strip())

bayesValues = trainNaiveBayes("bayes")
